const getParams = __PARSE_URL_VARS__();

const getCookie = name => {
  // return
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
}

const setCookie = (cname, cvalue) => document.cookie = cname + "=" + cvalue + ";path=/";

if (!getCookie('locks')) {
  setCookie('locks', '{}');
}

const getSessionData = () => {
  const cData = getCookie('locks');
  try {
    const parsed = JSON.parse(cData);
    return parsed;
  } catch (err) {
    setCookie('locks', '{}');
  }
};

const sessionData = getSessionData() || {};

if (!sessionData.id) {
  fetch('session').then(function (response) {
    return response.json();
  }).then(function (data) {
    // This is the JSON from our response
    if (data.id) {
      setCookie('locks', JSON.stringify({
        id: data.id,
      }));
    }
  }).catch(function (err) {
    // There was an error
    console.warn('Something went wrong.', err);
  });
}

const frameOffsets = [
  [0, 0],
  [272, 0],
  [544, 0],
  [544, 252],
  [272, 252],
  [0, 252],
];

const points = [];

window.onmessage = function (e) {
  if (e.data) {
    try {
      const result = JSON.parse(e.data);
      const { questionIndex, completed, wires, token } = result;
      const frameOffset = frameOffsets[questionIndex - 1];
      if (completed) {
        const sessionData = getSessionData();
        if (typeof sessionData[questionIndex] === 'undefined') {
          // new thing unlocked
          sessionData[questionIndex] = token;
          setCookie('locks', JSON.stringify(sessionData));

          fetch(`eval?id=${getParams.id}`).then(function (response) {
            return response.json();
          }).then(function (data) {
            if (data.hash) {
              __POST_RESULTS__({
                resourceId: getParams.id || '1111',
                hash: data.hash,
                action: data.action,
              });
            }
          }).catch(function (err) {
            // There was an error
            console.warn('Something went wrong.', err);
          });
        }
        document.querySelector(`.pin${questionIndex}`).classList.add('completed');
      }
      (wires || []).forEach(wire => {
        (wire.path || []).forEach(pt => points.push(pt.map((comp, index) => comp + frameOffset[index])));
      });

    } catch (error) {

    }
  }
};


const effectsCanvas = document.querySelector('canvas.effects');
const ctx = effectsCanvas.getContext('2d');


const jitterLevel = 4;
const jitter = () => -(jitterLevel / 2) + (Math.random() * jitterLevel);

const renderEffects = () => {
  ctx.clearRect(0, 0, effectsCanvas.width, effectsCanvas.height);
  ctx.fillStyle = 'magenta';
  points.forEach(pt => {
    if (Math.random() > .8) {
      ctx.fillRect(pt[0] + jitter(), pt[1] + jitter(), 4, 4);
    }
  });
  window.requestAnimationFrame(renderEffects);
};

window.requestAnimationFrame(renderEffects);


// instructions

const instructionsElement = document.querySelector('.instructions');
const okayBtn = document.querySelector('button.okayBtn');
const helpBtn = document.querySelector('button.helpBtn');

const toggleHelp = () => instructionsElement.classList.toggle('hide');

okayBtn.addEventListener('click', toggleHelp);
helpBtn.addEventListener('click', toggleHelp);

if (Object.keys(sessionData || {}).length !== 0) {
  toggleHelp();
}
