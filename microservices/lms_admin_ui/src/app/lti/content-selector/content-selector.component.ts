import { Component, ViewChild, Inject } from '@angular/core';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { DomSanitizer } from '@angular/platform-browser';


@Component({
  selector: 'app-content-selector',
  templateUrl: './content-selector.component.html',
  styleUrls: ['./content-selector.component.scss']
})
export class ContentSelectorComponent {
  loadingIframe = true
  iframeUrl: any = null
  constructor(
    private sanitizer: DomSanitizer,
    public dialogRef: MatDialogRef<ContentSelectorComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any, public ltiService: LtiService
  ) {
    console.log(dialogData)
    this.getToolUrl()
    window.addEventListener('message', (e: MessageEvent) => {
      // Get the sent data
      console.log("coded", e.data)
      const data = e.data;
      const decoded = JSON.parse(data);
      console.log("decoded", decoded)
      this.dialogRef.close({ data: decoded });
    });
  }

  getToolUrl() {
    let data = this.dialogData.extra_data
    this.ltiService.contentSelectionLaunch(data.toolId, data.userId, data.contextId, data.contextType).subscribe(
      (response: any) => {
        this.loadingIframe = false
        this.iframeUrl = response.url
      }
    )
  }
  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

  getUrl(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url)
  }

}
