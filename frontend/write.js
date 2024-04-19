// 글쓰기 전송
const form = document.getElementById("write-form");
const handleSubmit = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime()); // 세계시간
  try {
    const res = await fetch("/item", {
      method: "POST",
      body,
    });
    const data = await res.json();

    if (data === "201") window.location.pathname = "/"; // 페이지 이동
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmit);
