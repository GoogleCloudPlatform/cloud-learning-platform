import { Component, ViewChild, Inject } from '@angular/core';
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatSort } from '@angular/material/sort';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { ToolFormComponent } from '../tool-form/tool-form.component';


interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-tools-list',
  templateUrl: './tools-list.component.html',
  styleUrls: ['./tools-list.component.scss']
})
export class ToolsListComponent {
  isLoadingData: boolean = true
  ltiToolsData = []
  dataSource = new MatTableDataSource(this.ltiToolsData);
  ltiDisplayedColumns: string[] = ['client_id', 'name', 'description', 'action'];

  constructor(public dialog: MatDialog, private ltiService: LtiService) { }
  @ViewChild(MatSort) sort: MatSort;

  ngOnInit(): void {
    this.dataSource.sort = this.sort;
    this.fetchLtiTools()
  }

  fetchLtiTools() {
    this.ltiService.getToolsList().subscribe((response: any) => {
      setTimeout(() => {
        this.isLoadingData = false
      }, 100);
      this.ltiToolsData = response.data
    })
  }

  openCreateToolDialog(): void {
    let ltiModalData: LooseObject = {}
    ltiModalData['mode'] = 'Create'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = {}

    const dialogRef = this.dialog.open(ToolFormComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
        this.fetchLtiTools()
      }
    });
  }

  openUpdateToolDialog(id, data): void {
    let ltiModalData: LooseObject = {}
    ltiModalData['mode'] = 'Update'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { id, ...data }

    const dialogRef = this.dialog.open(ToolFormComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
        this.fetchLtiTools()
      }
    });
  }

  openViewToolDialog(id, data): void {
    let ltiModalData: LooseObject = {}
    ltiModalData['mode'] = 'View'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { id, ...data }

    const dialogRef = this.dialog.open(ViewLtiDialog, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
    });
  }

  openDeleteDialog(id, name) {
    const dialogRef = this.dialog.open(DeleteLtiDialog, {
      width: '500px',
      data: { id, name }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
        this.fetchLtiTools()
      }
    });
  }
}


@Component({
  selector: 'delete-lti-tool-dialog',
  templateUrl: 'delete-lti-tool-dialog.html',
})
export class DeleteLtiDialog {
  constructor(
    public dialogRef: MatDialogRef<DeleteLtiDialog>,
    @Inject(MAT_DIALOG_DATA) public deleteDialogData: any, public ltiService: LtiService
  ) { }

  deleteTool() {
    this.ltiService.deleteTool(this.deleteDialogData.id).subscribe((res: any) => {
      if (res.success == true) {
        this.dialogRef.close({ data: 'success' });
      }
    })
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'view-lti-tool-dialog',
  templateUrl: 'view-lti-tool-dialog.html',
})
export class ViewLtiDialog {
  toolData: any;
  objectKeys = Object.keys
  constructor(
    public dialogRef: MatDialogRef<ViewLtiDialog>,
    @Inject(MAT_DIALOG_DATA) public viewDialogData: any, public ltiService: LtiService
  ) {
    this.toolData = viewDialogData.extra_data
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

// @Pipe({ name: 'keyValueUnsorted', pure: false  })
// export class KeyValuePipe implements PipeTransform {
//   transform(input: any): any {
//     let keys = [];
//     for (let key in input) {
//       if (input.hasOwnProperty(key)) {
//         keys.push({ key: key, value: input[key]});
//       }
//     }
//     return keys;
//   }
// }
