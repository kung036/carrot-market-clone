const form = document.querySelector("#login-form");

// 로그인하기
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  // 서버 요청
  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });

  // 로그인 요청 성공 시
  const data = await res.json();
  console.log(data);
  if (res.status === 200) {
    alert("로그인에 성공했습니다.");
    console.log(res.status);
    window.location.pathname = "/";
  } else if (res.status === 401) {
    // 로그인 실패 시
    alert("id 또는 password가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleSubmit);
