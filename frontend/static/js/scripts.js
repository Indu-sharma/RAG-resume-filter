document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var fileInput = document.getElementById('resume-files');
    var formData = new FormData();

    for (var i = 0; i < fileInput.files.length; i++) {
        formData.append("files", fileInput.files[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload/', true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            alert('Resumes uploaded successfully!');
        } else {
            alert('Upload failed.');
        }
    };
    xhr.send(formData);
});

document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var query = document.getElementById('search-query').value;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/search/?query=' + encodeURIComponent(query), true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var result = JSON.parse(xhr.responseText).results[0].message.content; 
            var chatContainer = document.getElementById('chat-container');
            chatContainer.innerHTML = ''; 
            var summary = extractSummary(result);
            var skillMatch = extractSkillMatch(result);
            var experience = extractExperience(result);
            var summaryMessage = document.createElement('div');
            summaryMessage.classList.add('chat-message');
            summaryMessage.textContent = `${summary}`;
            chatContainer.appendChild(summaryMessage);
            if (skillMatch) {
                var skillMatchMessage = document.createElement('div');
                skillMatchMessage.classList.add('chat-message');
                skillMatchMessage.innerHTML = `<strong>Skill Match Percentage:</strong> ${skillMatch}<br>`;
                chatContainer.appendChild(skillMatchMessage);
            }
            if (experience) {
                var experienceMessage = document.createElement('div');
                experienceMessage.classList.add('chat-message');
                experienceMessage.textContent = `Experience: ${experience}`;
                chatContainer.appendChild(experienceMessage);
            }
        } else {
            alert('Search failed.');
        }
    };
    xhr.send();
});
function extractSummary(content) {
    const lines = content.split('\n');
    return lines.slice(0, 3).join('\n');
}

function extractSkillMatch(content) {
    var skillMatchMatch = content.match(/Skill Match Percentage:\s*(\d+)%/);
    return skillMatchMatch ? skillMatchMatch[1] : null; 
}

function extractExperience(content) {
    var experienceMatch = content.match(/Experience:(.*?)(\n|$)/);
    return experienceMatch ? experienceMatch[1].trim() : null; 
}
