import { Component, Inject } from '@angular/core';
import { LtiService } from '../service/lti.service';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { DomSanitizer } from '@angular/platform-browser';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-content-selector',
  templateUrl: './content-selector.component.html',
  styleUrls: ['./content-selector.component.scss']
})
export class ContentSelectorComponent {
  loadingIframe = true
  iframeUrl: any = null
  urlAlreadyLoaded: boolean = false

  constructor(
    private _snackBar: MatSnackBar,
    private sanitizer: DomSanitizer,
    public dialogRef: MatDialogRef<ContentSelectorComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any, public ltiService: LtiService
  ) {
    this.getToolUrl()
    window.addEventListener('message', (e: MessageEvent) => {
      // Get the sent data
      const data = e.data;
      const decoded = JSON.parse(data);
      this.dialogRef.close({ data: decoded });
    });
  }
  getToolUrl() {
    let data = this.dialogData.extra_data
    // this.ltiService.contentSelectionLaunch(data.toolId, data.userId, data.contextId, data.contextType).subscribe(
    //   (response: any) => {
    //     this.loadingIframe = false
    //     this.iframeUrl = this.getUrl(response.url)
    //   }
    // )
    this.iframeUrl = `${environment.ltiUrl}content-selection-launch-init?tool_id=${data.toolId}&user_id=${data.userId}&context_id=${data.contextId}&context_type=${data.contextType}`
  }

  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }

  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['green-snackbar'],
    });
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

  getUrl(url): any {
    if (!this.urlAlreadyLoaded) {
      this.urlAlreadyLoaded = true
      return this.sanitizer.bypassSecurityTrustResourceUrl(url)
    }
  }

}
