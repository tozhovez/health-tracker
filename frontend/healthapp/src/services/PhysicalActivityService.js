// services/PhysicalActivityService.js

export async function fetchPhysicalActivityData(userUuid) {
    try {
      const response = await fetch(`http://0.0.0.0:6565/api/physical-activity/${userUuid}?skip=0&limit=100`);
      if (!response.ok) {
        throw new Error("Ошибка загрузки данных физической активности");
      }
      return await response.json();
    } catch (error) {
      console.error("Ошибка при загрузке данных физической активности:", error);
      return [];
    }
  }
  