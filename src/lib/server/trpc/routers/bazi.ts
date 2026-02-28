import { router, publicProcedure, TRPCError } from '../init';
import { analyzeBaziInputSchema, analyzeBaziOutputSchema } from '../schemas';
import { analyzeBazi as analyzeBaziService } from '$lib/server/services/bazi';

export const baziRouter = router({
	analyze: publicProcedure
		.input(analyzeBaziInputSchema)
		.output(analyzeBaziOutputSchema)
		.query(({ input }) => {
			try {
				return analyzeBaziService({
					birth_date: input.birth_date,
					birth_time: input.birth_time,
					gender: input.gender,
					analysis_year: input.analysis_year,
					include_annual_luck: input.include_annual_luck,
					analysis_month: input.analysis_month,
					analysis_day: input.analysis_day,
					analysis_time: input.analysis_time,
					school: input.school,
					location: input.location,
					talisman_year_hs: input.talisman_year_hs,
					talisman_year_eb: input.talisman_year_eb,
					talisman_month_hs: input.talisman_month_hs,
					talisman_month_eb: input.talisman_month_eb,
					talisman_day_hs: input.talisman_day_hs,
					talisman_day_eb: input.talisman_day_eb,
					talisman_hour_hs: input.talisman_hour_hs,
					talisman_hour_eb: input.talisman_hour_eb,
				});
			} catch (error) {
				throw new TRPCError({
					code: 'INTERNAL_SERVER_ERROR',
					message: error instanceof Error ? error.message : 'BaZi analysis failed',
				});
			}
		}),
});
