// Sample data from the API
const knowledgeData = [
    {"knowledge_id": "1", "cluster_name": "Cluster 1", "num_folders": 3},
    {"knowledge_id": "2", "cluster_name": "Cluster 2", "num_folders": 2},
    // Add more knowledge clusters here
];

const folderData = {
    "1": [{"folder_name": "Folder 1", "source_type": "google_drive"}, {"folder_name": "Folder 2", "source_type": "microsoft_onedrive"}],
    "2": [{"folder_name": "Folder A", "source_type": "google_drive"}, {"folder_name": "Folder B", "source_type": "microsoft_onedrive"}],
    // Add more folders for each knowledge cluster
};

const sourcesData = [
    {"source_type": "google_drive", "display_name": "Google Drive"},
    {"source_type": "microsoft_onedrive", "display_name": "Microsoft OneDrive"},
    // Add more source types here
];

// Function to populate the knowledge list
function populateKnowledgeList() {
    const knowledgeList = document.getElementById('knowledgeList');
    knowledgeList.innerHTML = ''; // Clear existing list

    knowledgeData.forEach(item => {
        const listItem = document.createElement('a');
        listItem.href = '#';
        listItem.className = 'list-group-item list-group-item-action';
        listItem.dataset.knowledgeId = item.knowledge_id;
        listItem.innerHTML = `${item.cluster_name} <span class="badge bg-secondary">${item.num_folders} folders</span>`;
        knowledgeList.appendChild(listItem);
    });
}

// Function to populate the folder list for a knowledge cluster
function populateFolderList(knowledgeId) {
    const folderList = document.getElementById('folderList');
    folderList.innerHTML = ''; // Clear existing folder list

    folderData[knowledgeId].forEach(item => {
        const listItem = document.createElement('a');
        listItem.href = '#';
        listItem.className = 'list-group-item list-group-item-action';
        listItem.innerHTML = `${item.folder_name} (${item.source_type})`;
        folderList.appendChild(listItem);
    });
}

// Function to populate the source dropdown
function populateSourceDropdown() {
    const sourceDropdown = document.getElementById('sourceDropdown');
    sourceDropdown.innerHTML = '';
    sourcesData.forEach(item => {
        const option = document.createElement('option');
        option.value = item.source_type;
        option.text = item.display_name;
        sourceDropdown.appendChild(option);
    });
    sourceDropdown.style.display = 'block'; // Show the source dropdown
}

// Function to populate the folder dropdown based on the selected source
function populateFolderDropdown(selectedSource) {
    const folderDropdown = document.getElementById('folderDropdown');
    folderDropdown.innerHTML = '';

    // Implement the logic to fetch folders based on the selected source and populate the folder dropdown
    // For now, let's populate it with sample data
    const sampleFolders = [{"folder_id": "1", "folder_name": "Folder 1"}, {"folder_id": "2", "folder_name": "Folder 2"}];
    sampleFolders.forEach(item => {
        const option = document.createElement('option');
        option.value = item.folder_id;
        option.text = item.folder_name;
        folderDropdown.appendChild(option);
    });

    folderDropdown.style.display = 'block'; // Show the folder dropdown
}

// Function to show the Edit Container
function showEditContainer() {
    const knowledgeContainer = document.getElementById('knowledgeListContainer');
    const editContainer = document.getElementById('editContainer');
    knowledgeContainer.style.display = 'none';
    editContainer.style.display = 'block';
}

// Function to show the Knowledge List Container
function showKnowledgeListContainer() {
    const knowledgeContainer = document.getElementById('knowledgeListContainer');
    const editContainer = document.getElementById('editContainer');
    knowledgeContainer.style.display = 'block';
    editContainer.style.display = 'none';

}

// Function to show the Knowledge List Container
function loadKnowledgeListContainer() {
    showKnowledgeListContainer();
    populateKnowledgeList()
}

// Event listener for knowledge list item click
document.getElementById('knowledgeList').addEventListener('click', function (e) {
    const knowledgeId = e.target.dataset.knowledgeId;
    if (knowledgeId) {
        populateFolderList(knowledgeId);
        populateSourceDropdown(); // Populate source dropdown
        showEditContainer();
    }
});

// Event listener for create cluster button click
document.getElementById('createClusterBtn').addEventListener('click', function () {
    // Implement the logic to create a new knowledge cluster
    alert('Creating a new Knowledge Cluster...');
});

// Event listener for create folder button click
document.getElementById('createFolderBtn').addEventListener('click', function () {
    populateSourceDropdown();
    document.getElementById('sourceDropdown').style.display = 'block'; // Show the source dropdown
});

// Event listener for source selection
document.getElementById('sourceDropdown').addEventListener('change', function () {
    const selectedSource = this.value;
    populateFolderDropdown(selectedSource); // Populate folder dropdown based on selected source
});

// Event listener for folder selection and save
document.getElementById('folderDropdown').addEventListener('change', function () {
    const selectedFolder = this.value;
    const selectedSource = document.getElementById('sourceDropdown').value;
    // Implement the logic to save the selected folder
    alert(`Selected Folder: ${selectedFolder}, Selected Source: ${selectedSource}`);
});

// Event listener for back button in Edit Container
document.getElementById('backBtn').addEventListener('click', function () {
    showKnowledgeListContainer();
});


    const searchInput = $("#searchInput");
    const suggestionList = $("#suggestionList");

    searchInput.on("input", function() {
        const searchTerm = searchInput.val();

        if (searchTerm) {
            // Make a backend API call with the user-typed search term
            $.ajax({
                url: `http://127.0.0.1:8080/integration/load-folders?source_type=GOOGLE_DRIVE&search_term=${searchTerm}`,
                headers: {
                    'Authorization': 'token e013ba0de7a8867e31d21c112ea85b0be13a0ff7'
                },
                success: function(response) {
                    suggestionList.empty();
                    if (response.code === 200) {
                        const files = response.message.files;
                        files.forEach(function(file) {
                            const folderName = file.name;
                            const listItem = $("<li class='list-group-item'></li>").text(folderName);
                            suggestionList.append(listItem);
                        });
                    } else {
                        suggestionList.append("<li class='list-group-item'>No suggestions found</li>");
                    }
                },
                error: function() {
                    suggestionList.empty();
                    suggestionList.append("<li class='list-group-item'>Error fetching suggestions</li>");
                }
            });
        } else {
            // Clear the suggestion list if the search input is empty
            suggestionList.empty();
        }
    });



window.addEventListener('load', loadKnowledgeListContainer);
