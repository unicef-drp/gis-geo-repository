import React, {useState} from "react";
import '../styles/Uploader.scss';
import '../styles/RDU.styles.scss';
import Dropzone from 'react-dropzone-uploader'
import {
    Button,
    Card,
    CardContent,
    LinearProgress,
    TextField,
    Typography
} from "@mui/material";


function UploadComponent (props: any)  {
    const meta = props.meta
    const [level, setLevel] = useState(props.level)
    const [entityType, setEntityType] = useState(props.entityType)

    const handleBlur = (e: { currentTarget: any; }) => {
        const currentTarget = e.currentTarget.parentElement.parentElement.parentElement;
        setTimeout(() => {
            if (!currentTarget.contains(document.activeElement)) {
                props.updateLevelAndEntityType(meta.id, level, entityType)
            }
        }, 10);
    };

    return (
        <Card sx={{ minWidth: 730, marginTop: 1 }}>
            <CardContent>
                <Typography sx={{ fontSize: 14 }} color='text.secondary' gutterBottom>
                    {meta.type}
                </Typography>
                <Typography variant="h6" component="div">
                    {meta.name}
                </Typography>
                <TextField type="number" id={ meta.id + 'level' } label="Level" variant="filled" value={level} sx={{ marginRight: 1 }} onChange={(e) => {
                    const level = e.target.value;
                    setLevel(level);
                }} onBlur={handleBlur}/>
                <TextField id={ meta.id + 'entity-type' } label="Entity Type" variant="filled" value={entityType} onChange={(e) => {
                    const entityType = e.target.value;
                    setEntityType(entityType)
                }} onBlur={handleBlur}/>
                <LinearProgress variant="determinate" value={meta.percent} sx={{ marginTop: 2 }} />
                <Button variant="outlined" color="error" onClick={() => meta.remove()} sx={{ marginTop: 1 }}>
                  Remove
                </Button>
            </CardContent>
        </Card>
    )
}

interface Level {
  [layerId: string]: string;
}
interface EntityType {
  [layerId: string]: string;
}


function Uploader() {
    const [labelFormat, setLabelFormat] = useState('admin_{level}');
    const [codeFormat, setCodeFormat] = useState('code_{level}');
    const [dataset, setDataset] = useState('');
    const [entityTypes, setEntityTypes] = useState<EntityType | undefined>({})
    const [levels, setLevels] = useState<Level | undefined>({})
    const [error, setError] = useState('')

    // @ts-ignore
    const _csrfToken = csrfToken || '';

    // specify upload params and url for your files
    // @ts-ignore
    const getUploadParams = ({file, meta}) => {
        const body = new FormData()
        body.append('file', file)
        body.append('id', meta.id)
        body.append('uploadDate', meta.lastModifiedDate)
        const headers = {
            'Content-Disposition': 'attachment; filename=' + meta.name,
            'X-CSRFToken': _csrfToken
        }
        return {url: '/api/layer-upload/', body, headers}
    }

    // called every time a file's `status` changes
    // @ts-ignore
    const handleChangeStatus = ({meta, file}, status) => {
        console.log(status, meta, file)
        if (status === 'preparing') {
            const _levels = levels
            _levels[meta.id] = ''
            setLevels(_levels)
            const _entityTypes = entityTypes
            _entityTypes[meta.id] = ''
            setEntityTypes(_entityTypes)
        }
    }

    const updateLevelAndEntityType = (layerId: string, level: string, entityType: string) => {
        setLevels({ ...levels, [layerId]: level })
        setEntityTypes({ ...entityTypes, [layerId]: entityType })
    }

    // receives array of files that are done uploading when submit button is clicked
    const handleSubmit = (files: { meta: any; }[], allFiles: { remove: () => any; }[]) => {
        // allFiles.forEach((f: { remove: () => any; }) => f.remove())
        console.log(entityTypes)
        console.log(levels)

        const postData = {
            'entity_types': entityTypes,
            'levels': levels,
            'all_files': files.map((f: { meta: any; }) => f.meta),
            'dataset': dataset,
            'code_format': codeFormat,
            'label_format': labelFormat
        }

        fetch('/api/layers-process/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': _csrfToken
            },
            body: JSON.stringify(postData)
        }).then( response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        }).then(data => console.log(data)
        ).catch(
            error => {
                console.error('Error calling layers-process api :', error)
                setError(error)
            }
        ).finally(() => {
            allFiles.forEach((f: { remove: () => any; }) => f.remove())
        })
    }

    // @ts-ignore
    return (
        <div className="App">
            <div className='content-body'>
                <h3>Layer Uploader</h3>
                <div className='layer-format'>
                    <TextField id="label-format" label="Dataset" variant="outlined" value={dataset} onChange={(e) => setDataset(e.target.value)}/>
                    <TextField id="label-format" label="Label Format" variant="outlined" value={labelFormat} onChange={(e) => setLabelFormat(e.target.value)}/>
                    <TextField id="code-format" label="Pcode Format" variant="outlined" value={codeFormat} onChange={(e) => setCodeFormat(e.target.value)} />
                </div>
                <div className='uploader-container'>
                     <Dropzone
                         PreviewComponent={(props) => <UploadComponent key={props.meta.id} meta={props.meta} level={levels[props.meta.id]} entityType={entityTypes[props.meta.id]} updateLevelAndEntityType={updateLevelAndEntityType} /> }
                         getUploadParams={getUploadParams}
                         onChangeStatus={handleChangeStatus}
                         onSubmit={handleSubmit}
                         accept="image/*,audio/*,video/*"
                     />
                </div>
            </div>
        </div>
    )
}

export default Uploader;
