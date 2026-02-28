import { router } from './init';
import { healthRouter } from './routers/health';
import { profileRouter } from './routers/profile';
import { lifeEventRouter } from './routers/lifeEvent';
import { baziRouter } from './routers/bazi';
import { dongGongRouter } from './routers/dongGong';

export const appRouter = router({
	health: healthRouter,
	profile: profileRouter,
	lifeEvent: lifeEventRouter,
	bazi: baziRouter,
	dongGong: dongGongRouter,
});

export type AppRouter = typeof appRouter;
