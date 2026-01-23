// frontend/app.js
// AI Cinematic Preset Generator — FINAL STABLE VERSION

const form = document.getElementById("presetForm");
const statusText = document.getElementById("status");

const inputImageInput = document.getElementById("inputImage");
const referenceImageInput = document.getElementById("referenceImage");

const inputPreview = document.getElementById("inputPreview");
const referencePreview = document.getElementById("referencePreview");

/* ================= IMAGE PREVIEW ================= */

function previewImage(fileInput, previewEl) {
  const file = fileInput.files[0];
  if (!file) return;

  const name = file.name.toLowerCase();

  // Block HEIC (browser + backend safety)
  if (name.endsWith(".heic")) {
    previewEl.src = "";
    statusText.textContent =
      "❌ HEIC format not supported. Please upload JPG or PNG.";
    fileInput.value = "";
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    previewEl.src = reader.result;
  };
  reader.readAsDataURL(file);
}

inputImageInput.addEventListener("change", () =>
  previewImage(inputImageInput, inputPreview)
);

referenceImageInput.addEventListener("change", () =>
  previewImage(referenceImageInput, referencePreview)
);

/* ================= FORM SUBMIT ================= */

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  statusText.className = "loading";
  statusText.textContent = "🎬 Generating cinematic preset…";

  const formData = new FormData(form);

  try {
    const response = await fetch("http://127.0.0.1:8000/generate-preset", {
      method: "POST",
      body: formData,
    });

    // ⚠️ DO NOT ASSUME JSON
    const rawText = await response.text();

    let data;
    try {
      data = JSON.parse(rawText);
    } catch (err) {
      console.error("Raw server response:", rawText);
      throw new Error("Server returned non-JSON response");
    }

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Preset generation failed");
    }

    /* ================= SUCCESS ================= */

    statusText.className = "success";
    statusText.innerHTML = `
      ✅ Preset generated successfully <br>
      <a href="http://127.0.0.1:8000${data.download_url}"
         class="download-link"
         download>
         ⬇ Download Lightroom Preset
      </a>
    `;

  } catch (error) {
    console.error(error);

    // Friendly AI quota message
    if (
      error.message.includes("429") ||
      error.message.includes("RESOURCE_EXHAUSTED")
    ) {
      statusText.textContent =
        "⚠️ AI quota exceeded. Please wait a minute and try again.";
    } else {
      statusText.textContent = "❌ Failed to generate preset.";
    }

    statusText.className = "error";
  }
});
