
document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var tab = tabs[0];
        var url = new URL(tab.url);
        var videoId = url.searchParams.get('v');

        if (videoId) {
            // Call your Flask backend to get title and view count
            fetch(`http://127.0.0.1:5000/video-details?video_id=${videoId}`)
                .then(response => response.json())
                .then(data => {
                    // Update the popup HTML with title and view count
                    document.getElementById('video-title').textContent = `Video Title: ${data.title}`;
                    document.getElementById('view-count').textContent = `View Count: ${data.viewCount}`;

                    // Add event listener for the Summarize button
                    document.getElementById('summarize-button').addEventListener('click', function() {
                        // Call your Flask backend to get summary
                        fetch(`http://127.0.0.1:5000/summary-details?video_id=${videoId}`)
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(`HTTP error! Status: ${response.status}`);
                                }
                                return response.json();
                            })
                            .then(summaryData => {
                                // Update the popup HTML with summary
                                document.getElementById('summarized-text').textContent = `Summary: ${summaryData.summary}`;
                            })
                            .catch(error => {
                                console.error('Error fetching summary:', error);
                                return error.text();  // Log the HTML response
                            })
                            .then(htmlResponse => {
                                console.log('HTML Response:', htmlResponse);
                            });
                    });

                    // Add event listener for the Summarize button
                })
                .catch(error => console.error('Error fetching video details:', error));
        }
    });
});
