// ===== DAVYDOV STYLE HEADER JS =====

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('mobile-active');
            this.classList.toggle('active');
        });
    }
    
    // Header Scroll Effect
    let lastScrollTop = 0;
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Cookie Banner
    const cookieBanner = document.getElementById('cookieBanner');
    const cookieAccept = document.getElementById('cookieAccept');
    
    // Проверяем, было ли уже принято согласие
    if (cookieBanner && !localStorage.getItem('cookieConsent')) {
        cookieBanner.classList.add('show');
    }
    
    if (cookieAccept) {
        cookieAccept.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'accepted');
            cookieBanner.classList.remove('show');
        });
    }
    
    // Partners Carousel - Clone items for infinite scroll
    const partnersCarousel = document.querySelector('.partners-carousel');
    if (partnersCarousel) {
        const items = partnersCarousel.querySelectorAll('.partner-item');
        if (items.length > 0) {
            // Клонируем все элементы для бесконечной прокрутки
            items.forEach(item => {
                const clone = item.cloneNode(true);
                partnersCarousel.appendChild(clone);
            });
        }
    }
    
    // PDF Preview - Load first page of PDF files
    if (typeof pdfjsLib !== 'undefined') {
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        
        const pdfPreviews = document.querySelectorAll('.license-pdf-preview');
        pdfPreviews.forEach(canvas => {
            const pdfUrl = canvas.getAttribute('data-pdf-url');
            if (pdfUrl) {
                loadPdfPreview(canvas, pdfUrl);
            }
        });
    }
});

// Function to load and render first page of PDF
async function loadPdfPreview(canvas, pdfUrl) {
    // Add loading class
    canvas.classList.add('loading');
    
    try {
        const loadingTask = pdfjsLib.getDocument(pdfUrl);
        const pdf = await loadingTask.promise;
        const page = await pdf.getPage(1); // Get first page
        
        // Calculate scale to fit canvas container
        const container = canvas.parentElement;
        const containerWidth = container.clientWidth || 300;
        const containerHeight = container.clientHeight || 400;
        
        const viewport = page.getViewport({ scale: 1 });
        const scale = Math.min(containerWidth / viewport.width, containerHeight / viewport.height, 2);
        const scaledViewport = page.getViewport({ scale: scale });
        
        const context = canvas.getContext('2d');
        
        // Set canvas dimensions
        canvas.width = scaledViewport.width;
        canvas.height = scaledViewport.height;
        
        // Render PDF page to canvas
        const renderContext = {
            canvasContext: context,
            viewport: scaledViewport
        };
        
        await page.render(renderContext).promise;
        
        // Remove loading, add loaded class
        canvas.classList.remove('loading');
        canvas.classList.add('loaded');
    } catch (error) {
        console.error('Error loading PDF preview:', error);
        canvas.classList.remove('loading');
        
        // Show fallback icon if PDF fails to load
        const context = canvas.getContext('2d');
        const container = canvas.parentElement;
        const containerWidth = container.clientWidth || 300;
        const containerHeight = container.clientHeight || 400;
        
        canvas.width = containerWidth;
        canvas.height = containerHeight;
        
        context.fillStyle = '#f0f0f0';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = '#999';
        context.font = '20px Arial';
        context.textAlign = 'center';
        context.fillText('PDF', canvas.width / 2, canvas.height / 2 - 10);
        context.font = '14px Arial';
        context.fillText('Не удалось загрузить', canvas.width / 2, canvas.height / 2 + 20);
        
        canvas.classList.add('loaded');
    }
}

// License Modal Functions
function openLicenseModal(fileUrl, title, fileType) {
    const modal = document.getElementById('licenseModal');
    const modalImage = document.getElementById('licenseModalImage');
    const modalPdf = document.getElementById('licenseModalPdf');
    const modalTitle = document.getElementById('licenseModalTitle');
    const modalDownload = document.getElementById('licenseModalDownload');
    
    if (!modal) return;
    
    // Скрываем все элементы
    if (modalImage) modalImage.style.display = 'none';
    if (modalPdf) modalPdf.style.display = 'none';
    if (modalDownload) modalDownload.style.display = 'none';
    
    // Показываем соответствующий элемент в зависимости от типа файла
    if (fileType === 'image') {
        if (modalImage) {
            modalImage.src = fileUrl;
            modalImage.style.display = 'block';
        }
    } else if (fileType === 'pdf') {
        if (modalPdf) {
            modalPdf.src = fileUrl;
            modalPdf.style.display = 'block';
        }
        if (modalDownload) {
            modalDownload.href = fileUrl;
            modalDownload.style.display = 'inline-block';
        }
    }
    
    if (modalTitle) {
        modalTitle.textContent = title;
    }
    
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeLicenseModal() {
    const modal = document.getElementById('licenseModal');
    const modalPdf = document.getElementById('licenseModalPdf');
    
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
        
        // Останавливаем загрузку PDF при закрытии
        if (modalPdf) {
            modalPdf.src = '';
        }
    }
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeLicenseModal();
        closeCertificateModal();
    }
});

// Certificate Modal Functions
function openCertificateModal(imageUrl, title, number, issuer, issueDate, expiryDate) {
    const modal = document.getElementById('certificateModal');
    const modalImage = document.getElementById('certificateModalImage');
    const modalTitle = document.getElementById('certificateModalTitle');
    const modalNumber = document.getElementById('certificateModalNumber');
    const modalIssuer = document.getElementById('certificateModalIssuer');
    const modalIssueDate = document.getElementById('certificateModalIssueDate');
    const modalExpiryDate = document.getElementById('certificateModalExpiryDate');
    
    if (!modal) return;
    
    if (modalImage) modalImage.src = imageUrl;
    if (modalTitle) modalTitle.textContent = title;
    if (modalNumber) modalNumber.textContent = number;
    if (modalIssuer) modalIssuer.textContent = issuer;
    if (modalIssueDate) modalIssueDate.textContent = issueDate;
    if (modalExpiryDate) modalExpiryDate.textContent = expiryDate;
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeCertificateModal() {
    const modal = document.getElementById('certificateModal');
    
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}