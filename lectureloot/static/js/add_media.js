// dynamically adds inputs for image depending on how many are there
document.addEventListener('DOMContentLoaded', () => {
  const mediaForm = document.querySelector(".media-form");
  
  mediaForm.addEventListener("change", e => {
    const allFileInputs = mediaForm.querySelectorAll("input");
    const length = allFileInputs.length;
    allFileInputs.forEach((input,i) => {
      if (i == length-1 && input.value && i < 9) return addInput(length);
      if (i + 1 != length && !input.value) return removeInput(i);
    });
  });

  function addInput(n) {
    mediaForm.insertAdjacentHTML('beforeend', `
      <div class="media-${n}">
        <label for="id_form-${n}-file">File:</label>
        <input type="file" name="form-${n}-file" accept="image/*,video/*" id="id_form-${n}-file">
        <br>
      </div>
    `);
  }

  function removeInput(n) {
    mediaForm.querySelector(`.media-${n}`).remove();
    // reset all classes to start from 0 and go up one by one
    mediaForm.querySelectorAll("div").forEach((div, i) => {
      div.className = `media-${i}`;
    });
  }
});