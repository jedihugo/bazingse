import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const profiles = sqliteTable('profiles', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	birth_date: text('birth_date').notNull(),
	birth_time: text('birth_time'),
	gender: text('gender', { enum: ['male', 'female'] }).notNull(),
	place_of_birth: text('place_of_birth'),
	phone: text('phone'),
	created_at: text('created_at'),
	updated_at: text('updated_at')
});

export const lifeEvents = sqliteTable('life_events', {
	id: text('id').primaryKey(),
	profile_id: text('profile_id')
		.notNull()
		.references(() => profiles.id, { onDelete: 'cascade' }),
	year: integer('year').notNull(),
	month: integer('month'),
	day: integer('day'),
	location: text('location'),
	notes: text('notes'),
	is_abroad: integer('is_abroad', { mode: 'boolean' }).default(false),
	created_at: text('created_at'),
	updated_at: text('updated_at')
});
