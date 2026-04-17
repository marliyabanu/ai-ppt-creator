const API_URL = 'http://127.0.0.1:5000/api';
let currentOutline = [];
let currentStyle = 'professional';
let currentSlideCount = 20;
let currentPrompt = '';
let currentDownloadUrl = '';

// Page Navigation
function nextToPage2() {
    const prompt = document.getElementById('promptInput').value.trim();
    if (!prompt) {
        alert('Please enter a topic for your presentation');
        return;
    }
    
    currentPrompt = prompt;
    document.getElementById('page1').classList.remove('active');
    document.getElementById('page2').classList.add('active');
}

function prevToPage1() {
    document.getElementById('page2').classList.remove('active');
    document.getElementById('page1').classList.add('active');
}

// Slide Counter
function adjustSlides(delta) {
    let newCount = currentSlideCount + delta;
    if (newCount >= 10 && newCount <= 50) {
        currentSlideCount = newCount;
        document.getElementById('slideCount').textContent = currentSlideCount;
        
        const span = document.getElementById('slideCount');
        span.style.transform = 'scale(1.2)';
        setTimeout(() => {
            span.style.transform = 'scale(1)';
        }, 200);
    }
}

// Style Selection
function selectStyle(style) {
    currentStyle = style;
    
    document.querySelectorAll('.style-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    document.querySelector(`.style-card[data-style="${style}"]`).classList.add('selected');
}

// Generate Presentation
async function generatePresentation() {
    if (!currentPrompt) {
        alert('Please go back and enter a topic');
        return;
    }
    
    // Navigate to page 3
    document.getElementById('page2').classList.remove('active');
    document.getElementById('page3').classList.add('active');
    
    // Show generation status
    document.getElementById('generationStatus').style.display = 'block';
    document.getElementById('downloadSection').style.display = 'none';
    
    const statusMessages = [
        'Analyzing your topic...',
        'Creating slide structure...',
        'Writing content...',
        'Applying design...',
        'Finalizing presentation...'
    ];
    
    let messageIndex = 0;
    const statusInterval = setInterval(() => {
        if (messageIndex < statusMessages.length) {
            document.getElementById('statusMessage').textContent = statusMessages[messageIndex];
            messageIndex++;
        }
    }, 1500);
    
    try {
        // Step 1: Generate outline
        console.log("Generating outline...");
        const outlineResponse = await fetch(`${API_URL}/generate-outline`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: currentPrompt,
                num_slides: currentSlideCount
            })
        });
        
        if (!outlineResponse.ok) {
            throw new Error(`HTTP ${outlineResponse.status}: ${outlineResponse.statusText}`);
        }
        
        const outlineData = await outlineResponse.json();
        
        if (outlineData.error) {
            throw new Error(outlineData.error);
        }
        
        currentOutline = outlineData.outline;
        console.log(`Generated ${currentOutline.length} slides`);
        
        // Step 2: Generate PPT
        console.log("Generating PPT...");
        const pptResponse = await fetch(`${API_URL}/generate-ppt`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                outline: currentOutline,
                style: currentStyle,
                title: currentPrompt
            })
        });
        
        if (!pptResponse.ok) {
            throw new Error(`HTTP ${pptResponse.status}: ${pptResponse.statusText}`);
        }
        
        const pptData = await pptResponse.json();
        
        if (pptData.error) {
            throw new Error(pptData.error);
        }
        
        currentDownloadUrl = pptData.download_url;
        console.log("PPT generated, download URL:", currentDownloadUrl);
        
        // Clear interval and show success
        clearInterval(statusInterval);
        showSuccess();
        
    } catch (error) {
        console.error('Error:', error);
        clearInterval(statusInterval);
        document.getElementById('statusMessage').textContent = `Error: ${error.message}`;
        document.getElementById('statusMessage').style.color = '#ff0000';
        
        // Show retry button
        setTimeout(() => {
            if (confirm(`Failed to generate presentation: ${error.message}\n\nWould you like to try again?`)) {
                generatePresentation();
            } else {
                resetApp();
            }
        }, 1000);
    }
}

function showSuccess() {
    document.getElementById('generationStatus').style.display = 'none';
    document.getElementById('downloadSection').style.display = 'block';
    
    // Update presentation info
    const infoDiv = document.getElementById('pptInfo');
    infoDiv.innerHTML = `
        <strong>Topic:</strong> ${currentPrompt}<br>
        <strong>Number of Slides:</strong> ${currentOutline.length}<br>
        <strong>Style:</strong> ${currentStyle.charAt(0).toUpperCase() + currentStyle.slice(1)}<br>
        <strong>Generated:</strong> ${new Date().toLocaleString()}
    `;
    
    // Add confetti animation
    createConfetti();
}

function downloadPPT() {
    if (currentDownloadUrl) {
        console.log("Downloading from:", currentDownloadUrl);
        
        // Open download in new window
        window.open(currentDownloadUrl, '_blank');
        
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Downloading...';
        btn.disabled = true;
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 3000);
    } else {
        alert("No download URL available. Please generate the presentation again.");
    }
}

function resetApp() {
    currentOutline = [];
    currentStyle = 'professional';
    currentSlideCount = 20;
    currentPrompt = '';
    currentDownloadUrl = '';
    
    document.getElementById('promptInput').value = '';
    document.getElementById('slideCount').textContent = '20';
    
    document.getElementById('page3').classList.remove('active');
    document.getElementById('page1').classList.add('active');
    
    document.querySelectorAll('.style-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.querySelector('.style-card[data-style="professional"]').classList.add('selected');
}

function setExample(text) {
    document.getElementById('promptInput').value = text;
    document.getElementById('promptInput').focus();
    
    const input = document.getElementById('promptInput');
    input.style.transform = 'scale(1.02)';
    setTimeout(() => {
        input.style.transform = 'scale(1)';
    }, 200);
}

function createConfetti() {
    const colors = ['#000000', '#333333', '#666666', '#999999'];
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.width = '8px';
        confetti.style.height = '8px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * window.innerWidth + 'px';
        confetti.style.top = '-10px';
        confetti.style.opacity = Math.random();
        confetti.style.pointerEvents = 'none';
        confetti.style.zIndex = '9999';
        document.body.appendChild(confetti);
        
        const animation = confetti.animate([
            { transform: 'translateY(0px) rotate(0deg)', opacity: 1 },
            { transform: `translateY(${window.innerHeight}px) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: Math.random() * 2000 + 1000,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        });
        
        animation.onfinish = () => confetti.remove();
    }
}

// Check server health on load
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        console.log("Server health:", data);
        return true;
    } catch (error) {
        console.error("Server not reachable:", error);
        alert("Cannot connect to server. Please make sure the backend is running on http://127.0.0.1:5000");
        return false;
    }
}

// Run health check when page loads
window.addEventListener('load', () => {
    checkServerHealth();
});