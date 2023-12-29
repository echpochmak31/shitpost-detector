async function checkPost() {
    event.preventDefault();

    const postText = document.getElementById("message").value;

    if (postText.trim() !== "") {
        document.getElementById("loadingSpinner").style.display = "inline-block";

        const formData = new FormData();
        formData.append('message', postText);

        const response = await fetch("/check_post", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById("loadingSpinner").style.display = "none";
            window.location.href = `/result?status=${result.status}`;
        } else {
            console.error("Ошибка при выполнении запроса:", response.statusText);
        }
    }
}
