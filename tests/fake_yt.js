// Minimal mock of the YouTube IFrame Player API, served in place of
// https://www.youtube.com/iframe_api by the test suite. Mimics the parts the
// app uses: ready/error events, load/play/pause/stop, time/duration/state.
//
// Video IDs of the form "errNNNNNNNN" (err + 8 digits) fire onError with that
// code instead of playing. Everything else "plays": a 1120 s video whose
// current time advances on a wall-clock timer.
//
// window.__ytReadyDelay (ms, default 30) delays onReady so tests can create
// races. window.__ytLog records load requests. window.__ytPlayerInstance is
// the most recently constructed player.

window.__ytLog = [];

window.YT = {
  PlayerState: { UNSTARTED: -1, ENDED: 0, PLAYING: 1, PAUSED: 2, BUFFERING: 3, CUED: 5 },
  Player: function (elId, cfg) {
    const self = this;
    window.__ytPlayerInstance = self;
    self._events = (cfg && cfg.events) || {};
    self._state = -1;
    self._t = 0;
    self._dur = 0;
    self._timer = null;

    const el = document.getElementById(elId);
    if (el) {
      const f = document.createElement('iframe');
      f.id = elId;
      f.src = 'about:blank';
      el.replaceWith(f);
    }

    self._emit = function (name, data) {
      if (self._events[name]) self._events[name]({ target: self, data: data });
    };
    self._change = function (s) { self._state = s; self._emit('onStateChange', s); };
    self._load = function (id, play) {
      window.__ytLog.push('load:' + id);
      clearInterval(self._timer); self._timer = null;
      const m = /^err(\d{8})$/.exec(id || '');
      if (m) { self._state = -1; self._emit('onError', parseInt(m[1], 10)); return; }
      self._dur = 1120; self._t = 0;
      if (play) self.playVideo(); else self._change(5);
    };

    self.playVideo = function () {
      if (self._timer) return;
      self._timer = setInterval(function () { self._t += 0.1; }, 100);
      self._change(1);
    };
    self.pauseVideo = function () { clearInterval(self._timer); self._timer = null; self._change(2); };
    self.stopVideo = function () { clearInterval(self._timer); self._timer = null; self._t = 0; self._change(5); };
    self.loadVideoById = function (id) { self._load(id, true); };
    self.cueVideoById = function (id) { self._load(id, false); };
    self.seekTo = function (s) { self._t = s; };
    self.mute = function () {};
    self.unMute = function () {};
    self.getCurrentTime = function () { return self._t; };
    self.getDuration = function () { return self._dur; };
    self.getPlayerState = function () { return self._state; };
    self.addEventListener = function () {};
    self.destroy = function () { clearInterval(self._timer); };

    setTimeout(function () {
      // like the real API: the initial video is already loading/playing by the
      // time onReady fires, so a loadVideoById() from the ready handler wins
      self._load(cfg && cfg.videoId, ((cfg && cfg.playerVars) || {}).autoplay === 1);
      self._emit('onReady');
    }, window.__ytReadyDelay || 30);
  },
};

setTimeout(function () {
  if (window.onYouTubeIframeAPIReady) window.onYouTubeIframeAPIReady();
}, 0);
