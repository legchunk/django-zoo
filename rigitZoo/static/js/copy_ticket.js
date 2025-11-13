document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('copy-share-link');
    if (!btn) return;

    btn.addEventListener('click', async (e) => {
        e.preventDefault();

        const url = btn.dataset.url || btn.getAttribute('href') || window.location.href;
        const originalHtml = btn.innerHTML;
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(url);
            };

            btn.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
        } catch (err) {
            window.prompt('Copy this link', url);
        }
    });
});