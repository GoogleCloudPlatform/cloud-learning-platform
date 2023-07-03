Feature: Update all association groups with active program ID and its disciplines

	Scenario: Update all association groups with active program ID and its discipline IDs
		Given A user has permission to user management to update all association groups with new active program ID
			When API request is sent to update all association groups with the new program ID and its disciplines
				Then All association groups are updated with the new active program ID and its discipline IDs
