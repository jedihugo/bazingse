import { z } from 'zod';
import { eq } from 'drizzle-orm';
import { router, publicProcedure, TRPCError } from '../init';
import { profileCreateSchema, profileUpdateSchema } from '../schemas';
import { profiles } from '$lib/server/db/schema';

export const profileRouter = router({
	list: publicProcedure
		.input(
			z
				.object({
					skip: z.number().int().min(0).default(0),
					limit: z.number().int().min(1).max(10000).default(100),
				})
				.default({ skip: 0, limit: 100 }),
		)
		.query(async ({ ctx, input }) => {
			const rows = await ctx.db.query.profiles.findMany({
				with: { lifeEvents: true },
				limit: input.limit,
				offset: input.skip,
			});
			return rows.map((r) => ({
				...r,
				life_events: r.lifeEvents ?? null,
			}));
		}),

	get: publicProcedure
		.input(z.object({ id: z.string() }))
		.query(async ({ ctx, input }) => {
			const row = await ctx.db.query.profiles.findFirst({
				where: eq(profiles.id, input.id),
				with: { lifeEvents: true },
			});
			if (!row) throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
			return { ...row, life_events: row.lifeEvents ?? null };
		}),

	create: publicProcedure.input(profileCreateSchema).mutation(async ({ ctx, input }) => {
		const id = crypto.randomUUID();
		const now = new Date().toISOString();
		await ctx.db.insert(profiles).values({
			id,
			...input,
			birth_time: input.birth_time ?? null,
			place_of_birth: input.place_of_birth ?? null,
			phone: input.phone ?? null,
			created_at: now,
			updated_at: now,
		});
		const created = await ctx.db.query.profiles.findFirst({
			where: eq(profiles.id, id),
			with: { lifeEvents: true },
		});
		return { ...created!, life_events: created!.lifeEvents ?? null };
	}),

	update: publicProcedure
		.input(
			z.object({
				id: z.string(),
				data: profileUpdateSchema,
			}),
		)
		.mutation(async ({ ctx, input }) => {
			const existing = await ctx.db.query.profiles.findFirst({
				where: eq(profiles.id, input.id),
			});
			if (!existing)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });

			const now = new Date().toISOString();
			await ctx.db
				.update(profiles)
				.set({ ...input.data, updated_at: now })
				.where(eq(profiles.id, input.id));

			const updated = await ctx.db.query.profiles.findFirst({
				where: eq(profiles.id, input.id),
				with: { lifeEvents: true },
			});
			return { ...updated!, life_events: updated!.lifeEvents ?? null };
		}),

	delete: publicProcedure
		.input(z.object({ id: z.string() }))
		.mutation(async ({ ctx, input }) => {
			const existing = await ctx.db.query.profiles.findFirst({
				where: eq(profiles.id, input.id),
			});
			if (!existing)
				throw new TRPCError({ code: 'NOT_FOUND', message: 'Profile not found' });
			await ctx.db.delete(profiles).where(eq(profiles.id, input.id));
		}),
});
