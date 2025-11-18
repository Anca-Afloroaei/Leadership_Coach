

  import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from '@/components/ui/select'

  // 1. Add to your schema
  const formSchema = z
    .object({
      firstName: z.string().min(1, { message: 'First name is required.' }),
      // ... other fields ...
      role: z.string().min(1, { message: 'Please select a role.' }), // ← New field
    })

  // 2. Add to defaultValues
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      firstName: '',
      // ... other fields ...
      role: '', // ← New field
    },
  })

  // 3. Use FormField with Select
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
            <SelectItem value="user">User</SelectItem>
            <SelectItem value="admin">Admin</SelectItem>
            <SelectItem value="moderator">Moderator</SelectItem>
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