export const Role = {
  EXECUTIVE: "executive",
  MANAGER: "manager",
  ENTREPRENEUR: "entrepreneur",
  COACH: "coach",
} as const;

export type Role = typeof Role[keyof typeof Role];