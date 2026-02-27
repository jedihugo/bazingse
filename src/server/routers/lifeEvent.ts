import { z } from 'zod';
import { router, publicProcedure, TRPCError } from '../trpc';
import { lifeEventCreateSchema, lifeEventUpdateSchema, lifeEventSchema } from '../schemas';
import * as db from '@/lib/db';

export const lifeEventRouter = router({
  get: publicProcedure
    .input(z.object({
      profileId: z.string(),
      eventId: z.string(),
    }))
    .output(lifeEventSchema)
    .query(async ({ input }) => {
      const event = await db.getLifeEvent(input.profileId, input.eventId);
      if (!event) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });
      }
      return event;
    }),

  create: publicProcedure
    .input(z.object({
      profileId: z.string(),
      data: lifeEventCreateSchema,
    }))
    .output(lifeEventSchema)
    .mutation(async ({ input }) => {
      const event = await db.addLifeEvent(input.profileId, input.data);
      if (!event) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
      }
      return event;
    }),

  update: publicProcedure
    .input(z.object({
      profileId: z.string(),
      eventId: z.string(),
      data: lifeEventUpdateSchema,
    }))
    .output(lifeEventSchema)
    .mutation(async ({ input }) => {
      const event = await db.updateLifeEvent(input.profileId, input.eventId, input.data);
      if (!event) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });
      }
      return event;
    }),

  delete: publicProcedure
    .input(z.object({
      profileId: z.string(),
      eventId: z.string(),
    }))
    .mutation(async ({ input }) => {
      const success = await db.deleteLifeEvent(input.profileId, input.eventId);
      if (!success) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });
      }
    }),
});
