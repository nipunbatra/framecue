"""Local file handling: indexing, playback, sidecar attach, metadata rendering."""

from conftest import add_files, demo_file

# minimal bytes: enough to become an item; tests that need playback use demo/
FAKE_MP4 = (b"\x00\x00\x00\x18ftypmp42", )
VTT = b"WEBVTT\n\n00:00.000 --> 59:59.000\nHi from VTT\n"
SRT = b"1\n00:00:00,000 --> 00:59:00,000\nHello SRT\n"


def fake_video(name="clip.mp4"):
    return (name, "video/mp4", FAKE_MP4[0])


def test_demo_video_plays_with_synced_subs_and_meta(page, http_root):
    page.goto(f"{http_root}/app.html")
    page.set_input_files("#fileInput", [demo_file("demo-lecture.mp4"),
                                        demo_file("demo-lecture.vtt"),
                                        demo_file("demo-lecture.json")])
    page.wait_for_function("items.length === 1 && activeIdx === 0")
    page.wait_for_function("video.currentTime > 0.3")
    assert "Lecture" in page.text_content("#meta")
    assert "/" in page.text_content("#clock")
    # seek into the middle of a real cue; the overlay must show exactly that cue
    result = page.evaluate("""async () => {
        video.pause();
        const cue = cues[1];
        video.currentTime = (cue.start + cue.end) / 2;
        await new Promise(r => setTimeout(r, 300));
        return { expected: cue.text.split('\\n').join(''),
                 got: document.querySelector('#subs').textContent };
    }""")
    assert result["got"] == result["expected"]


def test_srt_sidecar_attaches_to_existing_item(app):
    add_files(app, fake_video())
    app.wait_for_function("items.length === 1 && activeIdx === 0")
    add_files(app, ("clip.srt", "application/x-subrip", SRT))
    app.wait_for_function("cues.length === 1")
    app.wait_for_function("document.querySelector('#subs').textContent === 'Hello SRT'")
    assert app.locator("#list .item .tag.sub").text_content() == "subtitles"


def test_vtt_and_json_sidecars_attach_live(app):
    add_files(app, fake_video())
    app.wait_for_function("items.length === 1")
    add_files(app, ("clip.vtt", "text/vtt", VTT),
                   ("clip.json", "application/json", b'{"Title": "T1"}'))
    app.wait_for_function("document.querySelector('#subs').textContent === 'Hi from VTT'")
    app.wait_for_function("document.querySelector('#meta').textContent.includes('T1')")
    tags = app.locator("#list .item .tags").text_content()
    assert "subtitles" in tags and "meta·json" in tags


def test_srt_paired_with_video_in_one_pick(app):
    add_files(app, fake_video("talk.mp4"), ("talk.srt", "text/plain", SRT))
    app.wait_for_function("cues.length === 1")


def test_alert_when_no_playable_videos(app):
    messages = []
    app.once("dialog", lambda d: (messages.append(d.message), d.accept()))
    add_files(app, ("orphan.vtt", "text/vtt", VTT))
    app.wait_for_timeout(200)
    assert messages and "No playable videos" in messages[0]
    assert app.evaluate("items.length") == 0


def test_index_files_grouping(app):
    res = app.evaluate("""() => {
        const mk = n => new File(['x'], n);
        const { videos, orphans } = indexFiles([
            mk('a.mp4'), mk('a.vtt'), mk('a.json'), mk('a.txt'),
            mk('b.webm'), mk('b.txt'),
            mk('c.vtt'),
            mk('notes.pdf'),
        ]);
        return { v: videos.map(v => [v.name, !!v.vtt, v.metaType]),
                 o: orphans.map(o => o.base) };
    }""")
    assert res["v"] == [["a", True, "json"], ["b", False, "txt"]]  # json wins over txt
    assert res["o"] == ["c"]                                       # pdf is not a sidecar


def test_adding_more_files_keeps_active_selection(app):
    add_files(app, fake_video("bbb.mp4"))
    app.wait_for_function("activeIdx === 0")
    add_files(app, fake_video("aaa.mp4"))  # sorts before the active one
    app.wait_for_function("items.length === 2")
    assert app.evaluate("items[activeIdx].name") == "bbb"


def test_filename_with_html_is_not_injected(app):
    add_files(app, fake_video("<img src=x onerror=window.__pwned=1>.mp4"))
    app.wait_for_function("items.length === 1")
    assert app.evaluate("window.__pwned") is None
    assert app.locator("#list .item .name").text_content() == "<img src=x onerror=window.__pwned=1>"
    assert app.locator("#list .item .name img").count() == 0


def test_render_meta_variants(app):
    # BOM-prefixed JSON object still renders as key/value lines
    app.evaluate("() => renderMeta('\\uFEFF{\"A\": \"1\"}', 'json')")
    assert app.text_content("#meta").strip() == "A: 1"
    # valid JSON that is not an object renders raw, not as bogus key/value lines
    app.evaluate("() => renderMeta('\"just text\"', 'json')")
    assert app.text_content("#meta") == '"just text"'
    app.evaluate("() => renderMeta('[1,2,3]', 'json')")
    assert app.text_content("#meta") == "[1,2,3]"
    # invalid JSON falls back to raw text
    app.evaluate("() => renderMeta('{oops', 'json')")
    assert app.text_content("#meta") == "{oops"
    # nested values are stringified
    app.evaluate("() => renderMeta('{\"A\": {\"x\": 1}}', 'json')")
    assert app.text_content("#meta").strip() == 'A: {"x":1}'
    # .txt shown verbatim
    app.evaluate("() => renderMeta('line1\\nline2', 'txt')")
    assert app.text_content("#meta") == "line1\nline2"


def test_unplayable_video_shows_codec_message(app):
    add_files(app, fake_video())
    app.wait_for_function("!placeholder.classList.contains('hidden')")
    assert "Cannot play this file" in app.text_content("#placeholder")
