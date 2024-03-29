/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { SearchIcon } from "@heroicons/react/outline";
import lunr from "lunr";
import debounce from "lodash.debounce";
import { omit } from "ramda";
import { MutableRefObject } from "react";

export type ISearchResults = {
  query: string;
  result: lunr.Index.Result[];
};

const Search = ({
  inputRef,
  placeholder,
  documents,
  refField,
  handleQuery,
  omittedFields,
}: {
  inputRef?: MutableRefObject<null>,
  placeholder?: string;
  documents: Record<string, string>[];
  refField: string;
  handleQuery: (res: ISearchResults) => void;
  omittedFields?: string[];
}) => {
  if (!documents) return <></>;

  const searchIndex = lunr(function () {
    this.ref(refField);
    this.field("text");
    const builder = this;
    documents.forEach((doc) => {
      // Build a string with all values for searching against
      const stringRep = Object.values(omit(omittedFields || [], doc)).join(" ");
      const indexedDoc = {
        [refField]: doc[refField],
        text: stringRep,
      };
      builder.add(indexedDoc);
    });
  });

  const onChange = debounce((e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    handleQuery({
      query,
      result: searchIndex.search(query),
    });
  }, 200);

  return (
    <div className="relative">
      <SearchIcon className="h-6 absolute mt-3 ml-3 text-base-content" />
      <input
        ref={inputRef ?? null}
        type="text"
        placeholder={placeholder || "Search"}
        className="input px-10 py-3 w-full"
        onChange={onChange}
      />
    </div>
  );
};

export default Search;
