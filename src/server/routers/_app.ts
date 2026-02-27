import { router } from '../trpc';
import { healthRouter } from './health';
import { profileRouter } from './profile';
import { lifeEventRouter } from './lifeEvent';
import { baziRouter } from './bazi';
import { dongGongRouter } from './dongGong';

export const appRouter = router({
  health: healthRouter,
  profile: profileRouter,
  lifeEvent: lifeEventRouter,
  bazi: baziRouter,
  dongGong: dongGongRouter,
});

export type AppRouter = typeof appRouter;
