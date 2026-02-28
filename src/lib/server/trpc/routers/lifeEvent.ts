import { z } from 'zod';
import { eq, and } from 'drizzle-orm';
import { router, publicProcedure, TRPCError } from '../init';
import { lifeEventCreateSchema, lifeEventUpdateSchema } from '../schemas';
import { lifeEvents, profiles } from '$lib/server/db/schema';

export const lifeEventRouter = router({
	get: publicProcedure
		.input(
			z.object({
				profileId: z.string(),
				eventId: z.string(),
			}),
		)
		.query(async ({ ctx, input }) => {
			const event = await ctx.db.query.lifeEvents.findFirst({
				where: and(
					eq(lifeEvents.id, input.eventId),
					eq(lifeEvents.profile_id, input.profileId),
				),
			});
			if (!event)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });
			return event;
		}),

	create: publicProcedure
		.input(
			z.object({
				profileId: z.string(),
				data: lifeEventCreateSchema,
			}),
		)
		.mutation(async ({ ctx, input }) => {
			const profile = await ctx.db.query.profiles.findFirst({
				where: eq(profiles.id, input.profileId),
			});
			if (!profile)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });

			const id = crypto.randomUUID();
			const now = new Date().toISOString();
			await ctx.db.insert(lifeEvents).values({
				id,
				profile_id: input.profileId,
				...input.data,
				created_at: now,
				updated_at: now,
			});
			const created = await ctx.db.query.lifeEvents.findFirst({
				where: eq(lifeEvents.id, id),
			});
			return created!;
		}),

	update: publicProcedure
		.input(
			z.object({
				profileId: z.string(),
				eventId: z.string(),
				data: lifeEventUpdateSchema,
			}),
		)
		.mutation(async ({ ctx, input }) => {
			const existing = await ctx.db.query.lifeEvents.findFirst({
				where: and(
					eq(lifeEvents.id, input.eventId),
					eq(lifeEvents.profile_id, input.profileId),
				),
			});
			if (!existing)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });

			const now = new Date().toISOString();
			await ctx.db
				.update(lifeEvents)
				.set({ ...input.data, updated_at: now })
				.where(eq(lifeEvents.id, input.eventId));

			const updated = await ctx.db.query.lifeEvents.findFirst({
				where: eq(lifeEvents.id, input.eventId),
			});
			return updated!;
		}),

	delete: publicProcedure
		.input(
			z.object({
				profileId: z.string(),
				eventId: z.string(),
			}),
		)
		.mutation(async ({ ctx, input }) => {
			const existing = await ctx.db.query.lifeEvents.findFirst({
				where: and(
					eq(lifeEvents.id, input.eventId),
					eq(lifeEvents.profile_id, input.profileId),
				),
			});
			if (!existing)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Life event not found' });
			await ctx.db.delete(lifeEvents).where(eq(lifeEvents.id, input.eventId));
		}),
});
