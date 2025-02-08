'use client';

import * as React from 'react';
import '@/lib/env';

import Button from '@/components/buttons/Button';
import { SearchIcon } from 'lucide-react';


export default function HomePage() {
  const [search, setSearch] = React.useState<string>('');
  const [results, setResults] = React.useState<any[]>([]);

  const searchSyllabus = async (search: string) => {
    const res = await fetch(`http://3.230.154.38:3000/api/find_course?course_number=${search}`);
    const data = await res.json();
    console.log(data);
  };

  return (
    <main className='bg-white layout my-4'>
      <div>
        <h1 className='text-3xl font-bold'>Syllabus Searcher</h1>
 
        <div className='flex flex-row flex-nowrap space-x-4 mt-4'>
          <div className="w-full min-w-[200px]">
            <div className="relative">
              <input
                className="peer w-full bg-transparent placeholder:text-slate-400 text-slate-700 text-sm border border-slate-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-slate-400 hover:border-slate-300 shadow-sm focus:shadow"
                onChange={(e) => setSearch(e.target.value)}
              />
              <label className="absolute cursor-text bg-white px-1 left-2.5 top-2.5 text-slate-400 text-sm transition-all transform origin-left peer-focus:-top-2 peer-focus:left-2.5 peer-focus:text-xs peer-focus:text-slate-400 peer-focus:scale-90">
                Course Number
              </label>
            </div>
          </div>

          <Button leftIcon={SearchIcon} onClick={() => searchSyllabus(search)}>Search</Button>
        </div>
      </div>

      <div>
        <ol>
          {results.map((result) => (
            <li key={result.id}>
              <h2>{result.course_number}</h2>
              <p>{result.syllabus_href}</p>
            </li>
          ))}
        </ol>
      </div>
    </main>
  );
}
