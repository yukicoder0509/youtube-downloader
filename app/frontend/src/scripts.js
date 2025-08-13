import { getAvailableDirectories, downloadMedia } from "./request";

const youtubeHost = "youtube.com";

const url = new URL(window.location.href);
url.host = youtubeHost;
url.port = "";

const searchParams = new URLSearchParams(window.location.search);
let listParam = searchParams.get("list");

document.addEventListener("DOMContentLoaded", async () => {
  // find the url input element
  const urlInput = document.getElementById("url");

  // fill in the default url
  urlInput.value = url.href;

  // check if the url include play list
  if (listParam) {
    // handle playlist case
    document.getElementById("playlist-options").classList.remove("hidden");
    document.getElementById("list").checked = true;
  }

  // get the avaliable download directories
  const downloadDirectorySelect = document.getElementById("download-directory");
  const availableDirectories = await getAvailableDirectories();
  availableDirectories.forEach((dir) => {
    const option = document.createElement("option");
    option.value = dir;
    option.textContent = dir;
    downloadDirectorySelect.appendChild(option);
  });
});

// find the download form element
const downloadForm = document.getElementById("download-form");

// add event listener to the play list check box
const playlistCheckbox = document.getElementById("list");
playlistCheckbox.addEventListener("change", (event) => {
  const isChecked = event.target.checked;
  const hasListParam = searchParams.has("list");

  if (isChecked && !hasListParam) {
    searchParams.set("list", listParam);
  } else if (!isChecked && hasListParam) {
    searchParams.delete("list");
  }

  // Update the URL without reloading the page
  url.search = searchParams.toString();
  document.getElementById("url").value = url.toString();
});

// add submit event listener to the form
downloadForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const url = document.getElementById("url").value;
  const type = document.getElementById("type").value;
  const directory = document.getElementById("download-directory").value;

  // Show loading animation
  const messageDiv = document.getElementById("message");
  messageDiv.innerHTML = `<div id="loading-spinner" class="flex items-center gap-2"><svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path></svg>Downloading...</div>`;
  document.getElementById("download-button").disabled = true;

  downloadMedia(url, type, directory)
    .then((result) => {
      // Remove loading animation and show result
      messageDiv.innerHTML = `<span class='text-green-600'>Download complete!</span>`;
      // Optionally, handle result details here
    })
    .catch((err) => {
      messageDiv.innerHTML = `<span class='text-red-600'>Error: ${
        err.message || err
      }</span>`;
    })
    .finally(() => {
      document.getElementById("download-button").disabled = false;
    });
});
