import { Component, ViewChild, Inject } from '@angular/core';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'

@Component({
  selector: 'app-content-selector',
  templateUrl: './content-selector.component.html',
  styleUrls: ['./content-selector.component.scss']
})
export class ContentSelectorComponent {
  loadingIframe = true
  iframeUrl: any = null
  constructor(
    public dialogRef: MatDialogRef<ContentSelectorComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any, public ltiService: LtiService
  ) {
    console.log(dialogData)
    this.getToolUrl()
  }

  getToolUrl() {
    let data = this.dialogData.extra_data
    this.ltiService.contentSelectionLaunch(data.toolId, data.userId, data.contextId).subscribe(
      (response: any) => {
        this.loadingIframe = false
        this.iframeUrl = response.url
      }
    )
  }
  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }
}
