import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatLegacyMenuModule as MatMenuModule } from '@angular/material/legacy-menu';
import { MatLegacyButtonModule as MatButtonModule } from '@angular/material/legacy-button';
import { MatIconModule } from '@angular/material/icon';
import { MatLegacyTabsModule as MatTabsModule } from '@angular/material/legacy-tabs';
import { MatLegacyInputModule as MatInputModule } from '@angular/material/legacy-input';
import { MatLegacyFormFieldModule as MatFormFieldModule } from '@angular/material/legacy-form-field';
import { MatLegacyTooltipModule as MatTooltipModule } from '@angular/material/legacy-tooltip';
import { MatLegacyDialogModule as MatDialogModule } from '@angular/material/legacy-dialog';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatLegacySelectModule as MatSelectModule } from '@angular/material/legacy-select';
import { MatNativeDateModule } from '@angular/material/core';
import { MatLegacyProgressSpinnerModule as MatProgressSpinnerModule } from '@angular/material/legacy-progress-spinner';
import { MatLegacySnackBarModule as MatSnackBarModule } from '@angular/material/legacy-snack-bar';
import { MatLegacyCardModule as MatCardModule } from '@angular/material/legacy-card';
import { MatLegacyChipsModule as MatChipsModule } from '@angular/material/legacy-chips';
import { MatLegacyTableModule as MatTableModule } from '@angular/material/legacy-table';
import { MatDividerModule } from '@angular/material/divider';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatCheckboxModule } from '@angular/material/checkbox';


@NgModule({
    declarations: [
    ],
    imports: [
        CommonModule
    ],
    exports: [
        MatMenuModule,
        MatButtonModule,
        MatIconModule,
        MatTabsModule,
        MatInputModule,
        MatFormFieldModule,
        MatTooltipModule,
        MatDialogModule,
        MatDatepickerModule,
        MatSelectModule,
        MatNativeDateModule,
        MatProgressSpinnerModule,
        MatSnackBarModule,
        MatCardModule,
        MatChipsModule,
        MatTableModule,
        MatDividerModule,
        MatPaginatorModule,
        MatCheckboxModule
    ]
})
export class MaterialSharedModule { }