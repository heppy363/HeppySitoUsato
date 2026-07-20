import { defineStore } from "pinia";

export const useSearchFiltersStore = defineStore("searchFilters", {
  state: () => ({
    query: "",
    minPrice: null,
    maxPrice: null,
    platforms: [],
    sort: "relevance",
  }),
});
