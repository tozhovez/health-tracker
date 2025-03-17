export async function fetchUsers() {
    try {
      const response = await fetch("http://0.0.0.0:6565/api/users/?skip=0&limit=100");
      if (!response.ok) {
        throw new Error("Ошибка загрузки пользователей");
      }
      return await response.json();
    } catch (error) {
      console.error("Ошибка при загрузке пользователей:", error);
      return [];
    }
  }