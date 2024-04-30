const form = document.querySelector("#signup-form");

// 비밀번호가 같은지 확인
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  }

  return false;
};

// 회원가입한 정보를 서버로 보내기
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const div = document.querySelector("#info");
  if (checkPassword()) {
    // 서버 요청
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });

    // 서버 요청 성공 시
    const data = await res.json();
    if (data === 200) {
      // div.innerText = "회원가입에 성공했습니다!";
      // div.computedStyleMap.color = "blue";
      alert("회원가입에 성공했습니다.");
      // 로그인 화면 전환
      window.location.pathname = "/login.html";
    }
  } else {
    // 비밀번호가 입력되지 않은 경우
    div.innerText = "비밀번호가 같지 않습니다.";
    div.computedStyleMap.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
