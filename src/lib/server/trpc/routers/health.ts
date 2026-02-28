import { z } from 'zod';
import { router, publicProcedure } from '../init';

export const healthRouter = router({
	check: publicProcedure.output(z.object({ status: z.string() })).query(() => {
		return { status: 'ok' };
	}),
});
