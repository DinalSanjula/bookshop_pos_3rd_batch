const API = "http://127.0.0.1:8000/books";

const bookForm = document.getElementById("bookForm");
const bookTable = document.getElementById("bookTable");
const searchInput = document.getElementById("search");

// Load all books
async function loadBooks() {
    try {
        const response = await fetch(API);
        const books = await response.json();

        bookTable.innerHTML = "";

        books.forEach(book => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>Rs. ${book.price}</td>

                <td>
                    <button class="edit-btn" onclick="editBook(${book.id})">
                        Edit
                    </button>

                    <button class="delete-btn" onclick="deleteBook(${book.id})">
                        Delete
                    </button>
                </td>
            `;

            bookTable.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading books:", error);
    }
}

// Add new book
bookForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const book = {
        title: document.getElementById("title").value,
        author: document.getElementById("author").value,
        price: Number(document.getElementById("price").value),
        isbn: document.getElementById("isbn").value
    };

    console.log(book);

    try {
        await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(book)
        });

        bookForm.reset();
        loadBooks();

    } catch (error) {
        console.error("Error adding book:", error);
    }
});

// Delete book
async function deleteBook(id) {
    const confirmed = confirm("Delete this book?");

    if (!confirmed) return;

    try {
        await fetch(`${API}/${id}`, {
            method: "DELETE"
        });

        loadBooks();

    } catch (error) {
        console.error("Error deleting book:", error);
    }
}

// Update book
async function editBook(id) {
    const title = prompt("Enter Title:");
    const author = prompt("Enter Author:");
    const price = prompt("Enter Price:");
    const isbn = prompt("Enter isbn:");

    if (!title || !author || !price || !isbn) {
        return;
    }

    const book = {
        title,
        author,
        price: Number(price),
        isbn,
    };

    try {
        await fetch(`${API}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(book)
        });

        loadBooks();

    } catch (error) {
        console.error("Error updating book:", error);
    }
}

// Search books
searchInput.addEventListener("keyup", function () {
    const keyword = this.value.toLowerCase();

    const rows = bookTable.getElementsByTagName("tr");

    for (let row of rows) {
        const title = row.cells[1].innerText.toLowerCase();

        if (title.includes(keyword)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
});

// Load books when page opens
loadBooks();