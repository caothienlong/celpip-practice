# Project Brief: CELPIP Practice Platform

## Purpose

A professional, self-hosted CELPIP (Canadian English Language Proficiency Index Program) test practice platform that provides realistic exam simulation for Reading and Listening sections, with Writing and Speaking planned.

## Target Users

- **Test Takers**: Practice CELPIP tests anytime, track progress, identify weak areas
- **Teachers**: Assign practice tests, monitor student progress
- **Institutions**: Self-hosted, privacy-focused, customizable content

## Core Requirements

1. **Practice Mode**: Free navigation, view answer keys, auto-save progress, detailed explanations
2. **Test Mode**: Realistic exam simulation with timed sections, sequential navigation, scoring
3. **Listening Module**: State machine audio/video playback, per-question timers, split-pane layout
4. **Authentication**: OAuth (Google, Facebook) with guest mode fallback
5. **Data Persistence**: PostgreSQL (production) with JSON file fallback (local dev)
6. **Vocabulary Notes**: Per-user word saving with context, organized by test/skill/part
7. **Content-Driven**: JSON-based test data, auto-discovery, no code changes for new content

## Business Context

- **Version**: 5.0 (Production Ready)
- **License**: MIT
- **Deployment**: Render.com (web + PostgreSQL + Cloudinary for media)
- **Repository**: github.com:caothienlong/celpip-practice.git

## Success Criteria

- 10+ complete Reading tests with 380+ questions
- Functional Listening module with audio/video support
- Seamless Practice and Test mode experiences
- Working OAuth authentication with guest fallback
- Production deployment on Render.com
