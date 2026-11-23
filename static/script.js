const form = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const message = document.getElementById("message");
const taskList = document.getElementById("task-list");
const taskTemplate = document.getElementById("task-template");
const pager = document.getElementById("pager");
const prevButton = document.getElementById("prev-page");
const nextButton = document.getElementById("next-page");
const pageInfo = document.getElementById("page-info");
let editingId = null;
let currentPage = 1;
let totalPages = 1;

function showMessage(text, isError = false) {
    message.textContent = text;
    message.className = isError ? "error" : "";
}

// All API calls use this function. Show errors without clearing the form.
async function callApi(url, method = "GET", data) {
    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || "Request failed.");
        return result;
    } catch (error) {
        showMessage(error.message, true);
        return null;
    }
}

function resetForm() {
    editingId = null;
    form.reset();
    saveButton.textContent = "Add task";
    cancelButton.hidden = true;
}

function editTask(task) {
    if (saveButton.disabled) return;
    editingId = task.id;
    titleInput.value = task.title;
    priorityInput.value = task.priority;
    saveButton.textContent = "Save changes";
    cancelButton.hidden = false;
    titleInput.focus();
}

async function deleteTask(task, button) {
    if (saveButton.disabled || !confirm(`Delete "${task.title}"?`)) return;
    button.disabled = true;
    const result = await callApi(`/delete?id=${task.id}`, "DELETE");
    if (result) {
        if (editingId === task.id) resetForm();
        showMessage("Task deleted.");
        await loadTasks();
    }
    button.disabled = false;
}

// The server returns 6 tasks per page and corrects the page number if it is too high.
async function loadTasks() {
    const result = await callApi(`/tasks?page=${currentPage}`);
    if (!result) return;
    currentPage = result.page;
    totalPages = result.total_pages;

    pager.hidden = totalPages === 1;
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;

    taskList.replaceChildren();
    document.getElementById("empty-state").hidden = result.total > 0;
    for (const task of result.tasks) {
        const row = taskTemplate.content.firstElementChild.cloneNode(true);
        row.querySelector(".task-title").textContent = task.title;
        const priority = row.querySelector(".priority");
        priority.textContent = task.priority;
        priority.className = `priority ${task.priority.toLowerCase()}`;
        row.querySelector(".edit").onclick = () => editTask(task);
        const deleteButton = row.querySelector(".delete");
        deleteButton.onclick = () => deleteTask(task, deleteButton);
        taskList.append(row);
    }
}

form.onsubmit = async (event) => {
    event.preventDefault();
    if (saveButton.disabled) return;
    const data = { title: titleInput.value.trim(), priority: priorityInput.value };
    if (data.title.length < 2) {
        showMessage("Enter at least two characters for the title.", true);
        return;
    }
    saveButton.disabled = cancelButton.disabled = true;
    const url = editingId === null ? "/create" : `/update?id=${editingId}`;
    const result = await callApi(url, editingId === null ? "POST" : "PUT", data);
    if (result) {
        // New tasks are added at the end, so jump to the last page to show them.
        if (editingId === null) currentPage = totalPages + 1;
        resetForm();
        showMessage("Task saved.");
        await loadTasks();
    }
    saveButton.disabled = cancelButton.disabled = false;
};

cancelButton.onclick = resetForm;
prevButton.onclick = () => { currentPage--; loadTasks(); };
nextButton.onclick = () => { currentPage++; loadTasks(); };
loadTasks();
