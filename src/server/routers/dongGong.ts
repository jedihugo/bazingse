import { router, publicProcedure, TRPCError } from '../trpc';
import { dongGongCalendarInputSchema, dongGongCalendarOutputSchema } from '../schemas';
import { getDongGongCalendar as getDongGongCalendarService } from '../services/dong-gong';

export const dongGongRouter = router({
  calendar: publicProcedure
    .input(dongGongCalendarInputSchema)
    .output(dongGongCalendarOutputSchema)
    .query(({ input }) => {
      try {
        return getDongGongCalendarService(input);
      } catch (error) {
        throw new TRPCError({
          code: 'INTERNAL_SERVER_ERROR',
          message: error instanceof Error ? error.message : 'Dong Gong calendar generation failed',
        });
      }
    }),
});
