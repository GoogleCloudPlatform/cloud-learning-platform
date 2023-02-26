import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CreateCohortModalComponent } from '../create-cohort-modal/create-cohort-modal.component';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-cohort',
  templateUrl: './cohort.component.html',
  styleUrls: ['./cohort.component.scss']
})
export class CohortComponent implements OnInit {
  tempDescription: string = 'Paragraphs are the building blocks of papers. Many students define paragraphs in terms of length: a paragraph is a group of at least five sentences, a paragraph is half a page long, etc. In reality, though, the unity and coherence of ideas among sentences is what constitutes a paragraph. A paragraph is defined as “a group of sentences or a single sentence that forms a unit” (Lunsford and Connors 116). Length and appearance do not determine whether a section in a paper is a paragraph. For instance, in some styles of writing, particularly journalistic styles, a paragraph can be just one sentence long. Ultimately, a paragraph is a sentence or group of sentences that support one main idea. In this handout, we will refer to this as the “controlling idea,” because it controls what happens in the rest of the paragraph.'
  selectedCohort: any
  @Input() cohortList: any[]
  constructor(public router: Router, public dialog: MatDialog,) { }

  ngOnInit(): void {
  }
  setSelected(cohort: any) {
    this.selectedCohort = cohort
  }

  reRout(cohortid: any) {
    this.router.navigate(['/home/' + cohortid])
  }
  openEditModal() {
    let cohortModalData: LooseObject = {}
    cohortModalData['mode'] = 'Edit'
    cohortModalData['init_data'] = this.selectedCohort
    cohortModalData['extra_data'] = ''
    const dialogRef = this.dialog.open(CreateCohortModalComponent, {
      width: '500px',
      data: cohortModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        // this.getCohortList()
      }
    });
  }
  checkIfActive(start: string, end: string): boolean {
    let startDate = Date.parse(start)
    let endDate = Date.parse(end)
    let d = Date.now()
    if (d.valueOf() >= startDate.valueOf() && d.valueOf() <= endDate.valueOf()) {
      return true
    }
    else {
      return false
    }

  }
  ifUpcoming(start: string): boolean {
    let startDate = Date.parse(start)
    let d = Date.now()
    if (d.valueOf() < startDate.valueOf()) {
      return true
    }
    else {
      return false
    }
  }
}
