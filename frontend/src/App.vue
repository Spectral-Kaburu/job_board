<template>
  <div>
    <nav class="p-4 bg-blue-600 text-white flex gap-4">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/login">Login</RouterLink>
      <RouterLink to="/register">Register</RouterLink>
    </nav>

    <main class="p-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
</script>
