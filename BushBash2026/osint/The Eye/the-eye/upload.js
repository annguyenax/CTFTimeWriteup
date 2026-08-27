(() => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectedFileName = document.getElementById('selected-file-name');
    const dropZonePrompt = document.getElementById('drop-zone-prompt');
    const dropZonePreview = document.getElementById('drop-zone-preview');
    const previewImage = document.getElementById('preview-image');
    const previewUnavailable = document.getElementById('preview-unavailable');
    const previewFilename = document.getElementById('preview-filename');

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-primary');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-primary');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelected(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelected(fileInput.files[0]);
        }
    });

    function handleFileSelected(file) {
        const name = file.name;
        const ext = name.split('.').pop().toLowerCase();

        selectedFileName.textContent = `Selected: ${name}`;
        selectedFileName.classList.remove('d-none');

        dropZonePrompt.classList.add('d-none');
        dropZonePreview.classList.remove('d-none');
        const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
        previewFilename.textContent = `${name} (${sizeMB}MB)`;

        if (ext === 'jpg' || ext === 'jpeg' || ext === 'png') {
            previewUnavailable.classList.add('d-none');
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewImage.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            previewImage.classList.add('d-none');
            previewImage.src = '';
            previewUnavailable.classList.remove('d-none');
        }
    }
})();
