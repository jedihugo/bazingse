CREATE TABLE `life_events` (
	`id` text PRIMARY KEY NOT NULL,
	`profile_id` text NOT NULL,
	`year` integer NOT NULL,
	`month` integer,
	`day` integer,
	`location` text,
	`notes` text,
	`is_abroad` integer DEFAULT false,
	`created_at` text,
	`updated_at` text,
	FOREIGN KEY (`profile_id`) REFERENCES `profiles`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `profiles` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`birth_date` text NOT NULL,
	`birth_time` text,
	`gender` text NOT NULL,
	`place_of_birth` text,
	`phone` text,
	`created_at` text,
	`updated_at` text
);
