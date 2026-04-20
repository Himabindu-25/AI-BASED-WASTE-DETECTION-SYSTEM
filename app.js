const centersData = {

  Hyderabad: [
    { name: "Recycle One", link: "https://www.google.com/maps/search/Recycle+One+Hyderabad" },
    { name: "Crapbin", link: "https://www.google.com/maps/search/Crapbin+Hyderabad" }
  ],

  Madhapur: [
    { name: "Recytronics", link: "https://www.google.com/maps/search/Recytronics+Madhapur" }
  ],

  Gachibowli: [
    { name: "E-Waste Exchange", link: "https://www.google.com/maps/search/E-Waste+Exchange+Gachibowli" }
  ],

  Kukatpally: [
    { name: "Recycle India", link: "https://www.google.com/maps/search/Recycle+India+Hyderabad" }
  ],

  Ameerpet: [
    { name: "Eco Waste", link: "https://www.google.com/maps/search/Eco+Waste+Hyderabad" }
  ],

  BanjaraHills: [
    { name: "Green Planet Recycling", link: "https://www.google.com/maps/search/Green+Planet+Recycling+Hyderabad" }
  ],

  Secunderabad: [
    { name: "E-Waste Recyclers India", link: "https://www.google.com/maps/search/E+Waste+Recyclers+India+Hyderabad" }
  ],

  JubileeHills: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Jubilee+Hills+Hyderabad" }
  ],

  Dilsukhnagar: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Dilsukhnagar+Hyderabad" }
  ],

  LBnagar: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+LB+Nagar+Hyderabad" }
  ],

  Uppal: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Uppal+Hyderabad" }
  ],

  Miyapur: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Miyapur+Hyderabad" }
  ],

  Begumpet: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Begumpet+Hyderabad" }
  ],

  Tarnaka: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Tarnaka+Hyderabad" }
  ],

  Mehdipatnam: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Mehdipatnam+Hyderabad" }
  ],

  Warangal: [
    { name: "Warangal Recycling Center", link: "https://www.google.com/maps/search/Recycling+Warangal" }
  ],

  Karimnagar: [
    { name: "Karimnagar Waste Center", link: "https://www.google.com/maps/search/Recycling+Karimnagar" }
  ],

  Nizamabad: [
    { name: "Nizamabad Recycling Hub", link: "https://www.google.com/maps/search/Recycling+Nizamabad" }
  ],

  Mahbubnagar: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Mahbubnagar" }
  ],

  Khammam: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Khammam" }
  ],

  Adilabad: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Adilabad" }
  ],

  Nalgonda: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Nalgonda" }
  ],

  Suryapet: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Suryapet" }
  ],

  Siddipet: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Siddipet" }
  ],

  Medak: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Medak" }
  ],

  Sangareddy: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Sangareddy" }
  ],

  Vikarabad: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Vikarabad" }
  ],

  Kamareddy: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Kamareddy" }
  ],

  Jagitial: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Jagitial" }
  ],

  Mancherial: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Mancherial" }
  ],

  Yadadri: [
    { name: "Recycling Centers", link: "https://www.google.com/maps/search/recycling+center+Yadadri" }
  ]

};


// 📍 SHOW CENTERS
function showCenters() {
  let district = document.getElementById("district").value;
  let list = document.getElementById("centers");

  list.innerHTML = "";

  if (!district) {
    list.innerHTML = "<li>Select location</li>";
    return;
  }

  if (!centersData[district]) {
    list.innerHTML = `<li>
      <a href="https://www.google.com/maps/search/recycling+center+${district}" target="_blank">
        📍 Search Recycling Centers in ${district}
      </a>
    </li>`;
    return;
  }

  centersData[district].forEach(c => {
    let li = document.createElement("li");
    li.innerHTML = `<a href="${c.link}" target="_blank">📍 ${c.name}</a>`;
    list.appendChild(li);
  });
}


// 🔤 TEXT DETECTION
function detectText() {
  let text = document.getElementById("textInput").value;

  fetch("/detect_text", {
    method: "POST",
    body: JSON.stringify({ text }),
    headers: { "Content-Type": "application/json" }
  })
  .then(res => res.json())
  .then(data => showResult(data));
}


// 📁 IMAGE UPLOAD
document.getElementById("uploadForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  let file = document.getElementById("imageInput").files[0];
  let formData = new FormData();
  formData.append("image", file);

  let res = await fetch("/classify", {
    method: "POST",
    body: formData
  });

  let data = await res.json();
  showResult(data);
});


// 📷 CAMERA
function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => document.getElementById("video").srcObject = stream);
}

function stopCamera() {
  let video = document.getElementById("video");
  let stream = video.srcObject;
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
  }
}

function capture() {
  let video = document.getElementById("video");
  let canvas = document.createElement("canvas");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  let ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0);

  window.captured = canvas.toDataURL("image/png");
  document.getElementById("preview").src = window.captured;
}

function detect() {
  fetch("/detect_live", {
    method: "POST",
    body: JSON.stringify({ image: window.captured }),
    headers: { "Content-Type": "application/json" }
  })
  .then(res => res.json())
  .then(data => showResult(data));
}


// 🎯 RESULT
function showResult(data) {
  let steps = "<ol>" + data.steps.map(s => `<li>${s}</li>`).join("") + "</ol>";

  document.getElementById("result").innerHTML = `
    <h2>${data.type.toUpperCase()}</h2>
    <p><b>🗑 Bin:</b> ${data.bin}</p>
    <p><b>🔍 Detected:</b> ${data.detected}</p>
    <h4>♻️ Steps:</h4>
    ${steps}
  `;
}