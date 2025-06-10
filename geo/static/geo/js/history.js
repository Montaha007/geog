// history.js
document.addEventListener("DOMContentLoaded", function () {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const searchBtn = document.getElementById('searchBtn');
    const clearBtn = document.getElementById('clearBtn');
    const historyItems = document.querySelectorAll('.history-item');
    const resultsInfo = document.getElementById('resultsInfo');
    const noResults = document.getElementById('noSearchResults');
    const historyList = document.getElementById('history-list');

    function highlightText(text, searchTerm) {
        if (!searchTerm) return text;
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        return text.replace(regex, '<span class="highlight">$1</span>');
    }

    function updateResultsCount(visibleCount, totalCount) {
        if (visibleCount === totalCount) {
            resultsInfo.innerHTML = `Showing all ${totalCount} locations`;
        } else {
            resultsInfo.innerHTML = `Showing ${visibleCount} of ${totalCount} locations`;
        }
    }

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;
        let visibleCount = 0;

        // Clear previous highlights
        document.querySelectorAll('.search-text').forEach(el => {
            el.innerHTML = el.textContent;
        });

        historyItems.forEach(item => {
            const name = item.dataset.name;
            const type = item.dataset.type;
            const matchesSearch = !searchTerm || name.includes(searchTerm);
            const matchesCategory = selectedCategory === 'all' || type === selectedCategory;
            
            if (matchesSearch && matchesCategory) {
                item.style.display = 'block';
                visibleCount++;
                
                // Highlight search terms
                if (searchTerm) {
                    const titleEl = item.querySelector('.card-title');
                    titleEl.innerHTML = highlightText(titleEl.textContent, searchTerm);
                }
            } else {
                item.style.display = 'none';
            }
        });

        updateResultsCount(visibleCount, historyItems.length);
        
        // Show/hide no results message
        if (visibleCount === 0 && (searchTerm || selectedCategory !== 'all')) {
            noResults.style.display = 'block';
            historyList.style.display = 'none';
        } else {
            noResults.style.display = 'none';
            historyList.style.display = 'block';
        }
    }

    function clearSearch() {
        searchInput.value = '';
        categoryFilter.value = 'all';
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        performSearch();
    }

    // Event listeners
    searchBtn.addEventListener('click', performSearch);
    clearBtn.addEventListener('click', clearSearch);
    searchInput.addEventListener('input', performSearch);
    categoryFilter.addEventListener('change', performSearch);
    
    // Enter key support
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Quick filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            const now = new Date();
            
            historyItems.forEach(item => {
                const itemDate = new Date(item.dataset.created);
                let shouldShow = true;
                
                switch(filter) {
                    case 'today':
                        shouldShow = itemDate.toDateString() === now.toDateString();
                        break;
                    case 'week':
                        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                        shouldShow = itemDate >= weekAgo;
                        break;
                    case 'recent':
                        const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                        shouldShow = itemDate >= monthAgo;
                        break;
                }
                
                item.style.display = shouldShow ? 'block' : 'none';
            });
            
            // Update results count
            const visibleItems = Array.from(historyItems).filter(item => 
                item.style.display !== 'none'
            ).length;
            updateResultsCount(visibleItems, historyItems.length);
        });
    });

    // Initial results count
    updateResultsCount(historyItems.length, historyItems.length);
});