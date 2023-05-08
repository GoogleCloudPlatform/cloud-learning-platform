import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { ContentSelectorComponent } from '../content-selector/content-selector.component';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-create-assignment',
  templateUrl: './create-assignment.component.html',
  styleUrls: ['./create-assignment.component.scss']
})
export class CreateAssignmentComponent {
  toolForm: FormGroup;
  dialogData = {
    mode: "Create"
  }
  toolsList = []
  constructor(
    // public dialogRef: MatDialogRef<CreateAssignmentComponent>,
    // @Inject(MAT_DIALOG_DATA) public dialogData: any,
    public dialog: MatDialog,
    private fb: FormBuilder, private ltiService: LtiService) { }

  ngOnInit() {
    this.getAllTools()
    // if (this.dialogData.mode == "Create") {
    this.toolForm = this.fb.group({
      "tool_id": [null, Validators.required],
      "start_date": [new Date("5/10/2023")],
      "end_date": [new Date("5/10/2023")],
      "due_date": [new Date("5/10/2023")],
      "lti_assignment_title": ["something", (Validators.required)],
      "max_points": [55, Validators.required]
    });
    // } else {
    // let redirectUris = this.dialogData.extra_data.redirect_uris
    // if (typeof (redirectUris) == "object") {
    //   redirectUris = redirectUris.join(";")
    // }
    // this.toolForm = this.fb.group({
    //   "name": [this.dialogData.extra_data.name, Validators.required],
    //   "description": [this.dialogData.extra_data.description],
    //   "tool_url": [this.dialogData.extra_data.tool_url, Validators.required],
    //   "tool_login_url": [this.dialogData.extra_data.tool_login_url, Validators.required],
    //   "public_key_type": [this.dialogData.extra_data.public_key_type, (Validators.required)],
    //   "tool_public_key": [this.dialogData.extra_data.tool_public_key, Validators.required],
    //   "tool_keyset_url": [this.dialogData.extra_data.tool_keyset_url, Validators.required],
    //   "content_selection_url": [this.dialogData.extra_data.content_selection_url, Validators.required],
    //   "redirect_uris": [redirectUris, Validators.required],
    //   "enable_grade_sync": [this.dialogData.extra_data.enable_grade_sync, Validators.required],
    //   "enable_nrps": [this.dialogData.extra_data.enable_nrps, Validators.required],
    //   "custom_params": [this.dialogData.extra_data.custom_params, Validators.required],
    //   "validate_title_for_grade_sync": [this.dialogData.extra_data.validate_title_for_grade_sync, Validators.required]
    // });
    // }
  }

  onDropdownChange() {
    console.log(this.toolForm.value)
  }

  processFormInputs(values) {
    // convert redirect uris from str to list and make data ready to send to API
    const arr = values.redirect_uris.split(";")
    const redirect_uris = arr.map(element => {
      return element.trim();
    });
    const finalValues = { ...values, "redirect_uris": redirect_uris }
    return finalValues
  }

  onSubmit(toolForm) {
    console.log(toolForm.value)
    const data = this.processFormInputs(toolForm.value)
    console.log(data)
    if (this.dialogData.mode == "Create") {
      this.ltiService.postTool(data).subscribe(response => {
        console.log("response", response)
        // this.dialogRef.close({ data: 'success' })
      })
    } else {
      // console.log("this.dialogData.extra_data", this.dialogData.extra_data)
      // this.ltiService.updateTool(this.dialogData.extra_data.id, data).subscribe(response => {
      //   console.log("response", response)
      //   this.dialogRef.close({ data: 'success' })
      // })
    }
  }

  fetchData(id) {
    const data = this.ltiService.getToolData(id).subscribe((response: any) => {
      return response.data
    })
  }

  openContentSelector(toolForm) {
    console.log(toolForm.value)
    let ltiModalData: LooseObject = {}
    ltiModalData['mode'] = 'Open'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = {
      contextId: "LS5TfQ4Q5UAV1SCDW3ZE",
      toolId: toolForm.value.tool_id,
      userId: "vcmt4ZemmyFm59rDzl1U"
    }

    const dialogRef = this.dialog.open(ContentSelectorComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
      }
      console.log("result", result)
    });
  }

  getAllTools() {
    this.ltiService.getToolsList().subscribe((res: any) => {
      this.toolsList = res.data
    })
  }



}
