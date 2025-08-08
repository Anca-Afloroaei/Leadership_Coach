import { Role } from "@/types/role"

/** Matches FastAPI's UserRead model exactly */
export interface User {
  id: string
  first_name: string 
  last_name: string 
  email: string 
  role: Role 
  industry: string
  years_experience: number 
  created_at: Date
  updated_at: Date 
}
