import { z } from 'zod';
import { router, publicProcedure, TRPCError } from '../trpc';
import { profileCreateSchema, profileUpdateSchema, profileSchema } from '../schemas';
import * as db from '@/lib/db';

export const profileRouter = router({
  list: publicProcedure
    .input(z.object({
      skip: z.number().int().min(0).default(0),
      limit: z.number().int().min(1).max(10000).default(100),
    }).default({ skip: 0, limit: 100 }))
    .output(z.array(profileSchema))
    .query(async ({ input }) => {
      const profiles = await db.getProfiles(input.skip, input.limit);
      return profiles;
    }),

  get: publicProcedure
    .input(z.object({ id: z.string() }))
    .output(profileSchema)
    .query(async ({ input }) => {
      const profile = await db.getProfile(input.id);
      if (!profile) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
      }
      return profile;
    }),

  create: publicProcedure
    .input(profileCreateSchema)
    .output(profileSchema)
    .mutation(async ({ input }) => {
      return db.createProfile(input);
    }),

  update: publicProcedure
    .input(z.object({
      id: z.string(),
      data: profileUpdateSchema,
    }))
    .output(profileSchema)
    .mutation(async ({ input }) => {
      const profile = await db.updateProfile(input.id, input.data);
      if (!profile) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
      }
      return profile;
    }),

  delete: publicProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ input }) => {
      const success = await db.deleteProfile(input.id);
      if (!success) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
      }
    }),
});
