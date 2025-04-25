/**
 * ArtGen FastAPI Service - Frontend JavaScript
 * Handles UI interactions and API calls for image generation
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const promptInput = document.getElementById('prompt');
    const modelSelect = document.getElementById('model');
    const sizeSelect = document.getElementById('size');
    const qualitySelect = document.getElementById('quality');
    const countInput = document.getElementById('count');
    const generateBtn = document.getElementById('generate-btn');
    const gallery = document.getElementById('gallery');
    const statusText = document.getElementById('status');
    const loadingIndicator = document.getElementById('loading');
    
    // Template for creating image elements
    const imageTemplate = document.getElementById('image-template');
    
    // Constants
    const API_URL = '/api/generate';

    /**
     * Show a toast notification
     * @param {string} message - The message to display
     * @param {string} type - The type of notification (success, error, warning)
     */
    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        toastContainer.appendChild(toast);
        
        // Auto-remove after 4 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toastContainer.removeChild(toast);
            }, 300);
        }, 4000);
    }

    /**
     * Set the application state (loading, error, success)
     * @param {string} state - The state to set
     * @param {string} message - Optional message to display
     */
    function setAppState(state, message = '') {
        switch (state) {
            case 'loading':
                loadingIndicator.classList.remove('hidden');
                gallery.classList.add('hidden');
                statusText.textContent = 'Generating...';
                generateBtn.disabled = true;
                break;
            case 'success':
                loadingIndicator.classList.add('hidden');
                gallery.classList.remove('hidden');
                statusText.textContent = message || 'Generation complete';
                generateBtn.disabled = false;
                break;
            case 'error':
                loadingIndicator.classList.add('hidden');
                statusText.textContent = message || 'An error occurred';
                generateBtn.disabled = false;
                break;
        }
    }

    /**
     * Generate images via the API
     */
    async function generateImages() {
        // Validate inputs
        if (!promptInput.value.trim()) {
            showToast('Please enter a prompt', 'error');
            return;
        }
        
        // Set loading state
        setAppState('loading');
        
        // Prepare request payload
        const payload = {
            model: modelSelect.value,
            prompt: promptInput.value.trim(),
            n: parseInt(countInput.value, 10),
            size: sizeSelect.value,
            quality: qualitySelect.value,
            format: 'png',
            background: 'auto'
        };
        
        try {
            // Send API request
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            // Handle non-successful responses
            if (!response.ok) {
                let errorMessage = 'Failed to generate images';
                
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (e) {
                    // If parsing JSON fails, use status text
                    errorMessage = `${errorMessage}: ${response.statusText}`;
                }
                
                throw new Error(errorMessage);
            }
            
            // Parse successful response
            const data = await response.json();
            
            // Clear existing gallery
            gallery.innerHTML = '';
            
            // Add each image to gallery
            data.images.forEach((img, index) => {
                // Create a new image container from template
                const imgContainer = imageTemplate.content.cloneNode(true);
                
                // Set the image source from base64 data
                const imgElement = imgContainer.querySelector('img');
                imgElement.src = `data:image/${img.filetype};base64,${img.b64_json}`;
                imgElement.alt = `Generated image ${index + 1} for "${payload.prompt}"`;
                
                // Set up download button
                const downloadBtn = imgContainer.querySelector('.download-btn');
                downloadBtn.addEventListener('click', () => {
                    downloadImage(img.b64_json, index, img.filetype);
                });
                
                // Add to gallery
                gallery.appendChild(imgContainer);
            });
            
            // Update UI state
            setAppState('success', `Generated ${data.images.length} image(s)`);
            showToast('Images generated successfully!');
            
        } catch (error) {
            console.error('Error generating images:', error);
            setAppState('error', error.message);
            showToast(error.message, 'error');
        }
    }

    /**
     * Download an image from base64 data
     * @param {string} base64Data - The base64 encoded image data
     * @param {number} index - The index of the image in the gallery
     * @param {string} fileType - The file type (png, jpeg)
     */
    function downloadImage(base64Data, index, fileType) {
        // Create a download link
        const link = document.createElement('a');
        link.href = `data:image/${fileType};base64,${base64Data}`;
        link.download = `generated-image-${Date.now()}-${index}.${fileType}`;
        
        // Trigger the download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Event listeners
    generateBtn.addEventListener('click', generateImages);
    
    // Handler for model changes to update available options
    modelSelect.addEventListener('change', function() {
        const model = this.value;
        
        // Update size options based on model
        if (model === 'dall-e-2') {
            // DALL-E 2 supports smaller sizes
            sizeSelect.innerHTML = `
                <option value="256x256">Small (256×256)</option>
                <option value="512x512">Medium (512×512)</option>
                <option value="1024x1024" selected>Large (1024×1024)</option>
            `;
        } else {
            // GPT Image and DALL-E 3 support larger sizes
            sizeSelect.innerHTML = `
                <option value="1024x1024" selected>Square (1024×1024)</option>
                <option value="1792x1024">Landscape (1792×1024)</option>
                <option value="1024x1792">Portrait (1024×1792)</option>
            `;
        }
        
        // Update quality options based on model
        if (model === 'dall-e-3') {
            qualitySelect.innerHTML = `
                <option value="standard" selected>Standard</option>
                <option value="hd">HD</option>
            `;
        } else if (model === 'gpt-image-1') {
            qualitySelect.innerHTML = `
                <option value="medium" selected>Medium</option>
            `;
        } else {
            // DALL-E 2 has no quality option, but we need to keep the UI consistent
            qualitySelect.innerHTML = `
                <option value="standard" selected>Standard</option>
            `;
        }
    });
}); 