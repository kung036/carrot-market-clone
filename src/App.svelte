<script>
  import Main from "./pages/Main.svelte";
  import Login from "./pages/Login.svelte";
  import Singup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/style.css";

  // router 설정
  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Singup,
    "/write": Write,
    "*": NotFound,
  };
</script>

<Router {routes} />
<!-- 
<main>
  <div>안녕하세요!</div>
</main>

<style>
  div {
    color : red;
  }
</style> -->
