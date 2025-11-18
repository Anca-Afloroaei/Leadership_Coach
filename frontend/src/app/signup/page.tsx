// frontend/src/app/signup/page.tsx
'use client'

import { useEffect, useState } from 'react'
import { useSession } from '@/contexts/SessionContext'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { DEFAULT_PROTECTED_ROUTE } from '@/config/routes'
import { apiSignup } from '@/services/auth'

// Shadcn/UI imports
import { toast } from 'sonner'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'

/**
 * Form schema with password confirmation validation
 */
const formSchema = z
  .object({
    firstName: z.string().min(1, { message: 'First name is required.' }),
    lastName: z.string().min(1, { message: 'Last name is required.' }),
    role: z.string().min(1, { message: 'Please select a role.' }),
    industry: z.string().min(1, { message: 'Please enter your industry.' }),
    years: z.coerce.number().min(0, { message: 'Please enter your years of experience.' }),
    email: z.string().email({ message: 'Please enter a valid email address.' }),
    password: z.string().min(6, { message: 'Password must be at least 6 characters.' }),
    confirmPassword: z.string().min(6, { message: 'Please retype your password.' }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match.',
    path: ['confirmPassword'],
  })

type FormValues = z.infer<typeof formSchema>

export default function SignupPage() {
  const { state, revalidateSession } = useSession()
  const router = useRouter()
  const [formError, setFormError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      firstName: '',
      lastName: '',
      role: '',
      industry: '',
      years: 0,
      email: '',
      password: '',
      confirmPassword: '',
    },
  })

  // Redirect authenticated users away from signup page
  useEffect(() => {
    if (state.isAuthenticated && state.user) {
      router.replace(DEFAULT_PROTECTED_ROUTE)
    }
  }, [state.isAuthenticated, state.user, router])

  async function onSubmit(values: FormValues) {
    setFormError(null)
    setIsSubmitting(true)

    try {
      // Call signup API
      await apiSignup(
        values.firstName,
        values.lastName,
        values.role,
        values.industry,
        values.years,
        values.email,
        values.password
      )

      // Revalidate session to update state immediately
      await revalidateSession();

      // Success! Show toast and redirect
      toast.success('Account created successfully! Welcome aboard!')

      // Use router.push for client-side navigation
      router.push(DEFAULT_PROTECTED_ROUTE)
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } }
      const message =
        error.response?.data?.detail || 'Sign up failed. Please try again.'

      setFormError(message)
      toast.error(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Show loading state during session validation
  if (state.isValidating) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-foreground"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Sign up for a new account</CardTitle>
        </CardHeader>
        <div className="flex items-center justify-center gap-1">
          <CardContent className="mr-0 pr-0">Existing users:
          </CardContent>
          <CardAction>
            <Button className="ml-0 pl-0 text-base text-muted-foreground underline" variant="link">Log In here</Button>
          </CardAction>
        </div>
        <CardContent>
          {formError && (
            <Alert variant="destructive" className="mb-4">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{formError}</AlertDescription>
            </Alert>
          )}
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {/* First Name Field */}
              <FormField
                control={form.control}
                name="firstName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter your first name"
                        autoComplete="given-name"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.firstName && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.firstName.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />
              {/* Last Name Field */}
              <FormField
                control={form.control}
                name="lastName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter your last name"
                        autoComplete="family-name"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.lastName && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.lastName.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />
              {/* Role Field Dropdown */}
              <FormField
                control={form.control}
                name="role"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Role</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isSubmitting}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a role" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="executive">Executive</SelectItem>
                        <SelectItem value="manager">Manager</SelectItem>
                        <SelectItem value="entrepreneur">Entrepreneur</SelectItem>
                        <SelectItem value="coach">Coach</SelectItem>
                      </SelectContent>
                    </Select>
                    {form.formState.errors.role && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.role.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />
              {/* Industry Field */}
              <FormField
                control={form.control}
                name="industry"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Industry</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter your industry"
                        autoComplete="industry"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.industry && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.industry.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />
              {/* Year of Experience Field */}
              <FormField
                control={form.control}
                name="years"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Years of Experience</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter your years of experince"
                        autoComplete="years"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.years && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.years.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />


              {/* Email Field */}
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input
                        type="email"
                        placeholder="Enter your email"
                        autoComplete="email"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.email && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.email.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />

              {/* Password Field */}
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        placeholder="Choose a strong password"
                        autoComplete="new-password"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.password && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.password.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />

              {/* Confirm Password Field */}
              <FormField
                control={form.control}
                name="confirmPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Retype Password</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        placeholder="Retype your password"
                        autoComplete="new-password"
                        disabled={isSubmitting}
                        {...field}
                      />
                    </FormControl>
                    {form.formState.errors.confirmPassword && (
                      <p className="mt-1 text-sm text-destructive">
                        {form.formState.errors.confirmPassword.message}
                      </p>
                    )}
                  </FormItem>
                )}
              />

              {/* Submit Button */}
              <div className="mt-6 flex justify-center">
                <Button
                  type="submit"
                  className="w-full"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Creating Account…' : 'Sign Up'}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  )
}