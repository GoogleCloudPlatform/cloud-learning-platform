import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { LtiService } from '../service/lti.service';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'

@Component({
  selector: 'app-tool-form',
  templateUrl: './tool-form.component.html',
  styleUrls: ['./tool-form.component.scss']
})
export class ToolFormComponent {
  toolForm: FormGroup;

  constructor(public dialogRef: MatDialogRef<ToolFormComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any,
    private fb: FormBuilder, private ltiService: LtiService) { }

  ngOnInit() {
    if (this.dialogData.mode == "Create") {
      this.toolForm = this.fb.group({
        "name": ["", Validators.required],
        "description": [""],
        "tool_url": ["", Validators.required],
        "tool_login_url": ["", Validators.required],
        "public_key_type": ["JWK URL", (Validators.required)],
        "tool_keyset_url": ["", Validators.required],
        "content_selection_url": [""],
        "redirect_uris": ["", Validators.required],
        "enable_grade_sync": [false],
        "enable_nrps": [false],
        "custom_params": [""],
        "validate_title_for_grade_sync": [false]
      });
    } else {
      let redirectUris = this.dialogData.extra_data.redirect_uris
      if (typeof (redirectUris) == "object") {
        redirectUris = redirectUris.join(";")
      }
      this.toolForm = this.fb.group({
        "name": [this.dialogData.extra_data.name, Validators.required],
        "description": [this.dialogData.extra_data.description],
        "tool_url": [this.dialogData.extra_data.tool_url, Validators.required],
        "tool_login_url": [this.dialogData.extra_data.tool_login_url, Validators.required],
        "public_key_type": [this.dialogData.extra_data.public_key_type, (Validators.required)],
        "tool_public_key": [this.dialogData.extra_data.tool_public_key, Validators.required],
        "tool_keyset_url": [this.dialogData.extra_data.tool_keyset_url, Validators.required],
        "content_selection_url": [this.dialogData.extra_data.content_selection_url],
        "redirect_uris": [redirectUris, Validators.required],
        "enable_grade_sync": [this.dialogData.extra_data.enable_grade_sync],
        "enable_nrps": [this.dialogData.extra_data.enable_nrps],
        "custom_params": [this.dialogData.extra_data.custom_params],
        "validate_title_for_grade_sync": [this.dialogData.extra_data.validate_title_for_grade_sync]
      });
    }
  }

  onDropdownChange() {
    if (this.toolForm.value.public_key_type === "JWK URL") {
      if (this.toolForm.contains("tool_public_key")) {
        this.toolForm.removeControl("tool_public_key")
      }
      this.toolForm.addControl("tool_keyset_url", new FormControl())
    } else {
      if (this.toolForm.contains("tool_keyset_url")) {
        this.toolForm.removeControl("tool_keyset_url")
      }
      this.toolForm.addControl("tool_public_key", new FormControl())
    }
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
        this.dialogRef.close({ data: 'success' })
      })
    } else {
      console.log("this.dialogData.extra_data", this.dialogData.extra_data)
      this.ltiService.updateTool(this.dialogData.extra_data.id, data).subscribe(response => {
        console.log("response", response)
        this.dialogRef.close({ data: 'success' })
      })
    }
  }

  fetchData(id) {
    const data = this.ltiService.getToolData(id).subscribe((response: any) => {
      return response.data
    })
  }

}
